import os
import requests
import pandas as pd
import re
import unicodedata

from bs4 import BeautifulSoup
from datetime import datetime
from app.extensions import db
from app.models.models import (
    Comercializacao, Producao, Importacao, Exportacao
)
from sqlalchemy import text

DOWNLOAD_URL = 'http://vitibrasil.cnpuv.embrapa.br/download/'
DOWNLOAD_DIR = 'downloads/'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_file_list():
    try:
        response = requests.get(DOWNLOAD_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        files = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('.csv'):
                files.append(href)
        return files
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {DOWNLOAD_URL}: {e}")
        # Retorna a lista de arquivos locais
        local_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.csv')]
        if local_files:
            print("Usando arquivos locais para sincronização.")
            return local_files
        else:
            print("Nenhum arquivo local disponível para sincronização.")
            return []

def get_remote_file_mod_time(filename):
    try:
        response = requests.head(f"{DOWNLOAD_URL}{filename}", timeout=10)
        response.raise_for_status()
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            return datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_local_file_mod_time(filepath):
    # Esta função retorna a data e hora da última modificação de um arquivo local, se ele existir.
    if os.path.exists(filepath):
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp)
    return None

def download_file(filename):
    try:
        url = f"{DOWNLOAD_URL}{filename}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo {filename}: {e}")
        return None

def remove_accents(input_str):
    # Normaliza a string para o formato NFD (Normalization Form Decomposition)
    nfkd_form = unicodedata.normalize('NFD', input_str)
    # Remove caracteres diacríticos
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return only_ascii

def process_csv(filepath, model):
    """
    - Ignorar as colunas 'id' e 'Produto' se existirem
    - Transformar de formato wide para long
    - Renomear 'control' para 'produto'
    - Converter 'produto' para string e remover acentos
    - Filtrar linhas onde 'produto' começa com duas letras seguidas de '_'
    - Filtrar valores não numéricos antes de converter o ano para inteiro
    - Converter a quantidade para float, tratando possíveis erros
    - Remover registros onde a quantidade é nula (opcional)
    - Inserir os dados na tabela correspondente
    """
    df = pd.read_csv(filepath, sep=';', encoding='utf-8')
    columns_to_drop = [col for col in ['id', 'Produto'] if col in df.columns]
    df = df.drop(columns=columns_to_drop)
    df_melted = df.melt(id_vars=['control'], var_name='ano', value_name='quantidade')
    df_melted.rename(columns={'control': 'produto'}, inplace=True)
    df_melted['produto'] = df_melted['produto'].astype(str).apply(remove_accents).str.lower()
    pattern = r'^[a-zA-Z]{2}_'
    df_filtered = df_melted[df_melted['produto'].str.match(pattern, na=False)].copy()
    df_filtered = df_filtered[pd.to_numeric(df_filtered['ano'], errors='coerce').notnull()]
    df_filtered.loc[:, 'ano'] = df_filtered['ano'].astype(int)
    df_filtered.loc[:, 'quantidade'] = pd.to_numeric(df_filtered['quantidade'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['quantidade'])
    df_filtered.to_sql(model.__tablename__, con=db.engine, if_exists='append', index=False)
 
def process_import_csv(filepath, model, extra_data):
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(filepath, sep=';', encoding='utf-8')

        # Ignorar a coluna 'Id'
        columns_to_drop = [col for col in ['Id'] if col in df.columns]
        df = df.drop(columns=columns_to_drop)

        # Renomear 'País' para 'pais'
        df.rename(columns={'País': 'pais'}, inplace=True)

        # Lidar com colunas duplicadas de anos
        # Pandas adiciona sufixos '.1', '.2', etc., para colunas duplicadas
        df.columns = df.columns.map(str)

        # Obter a lista de anos únicos
        year_columns = [col for col in df.columns if col not in ['pais']]
        years = sorted(set([col.replace('.1', '') for col in year_columns]))

        # Criar listas para armazenar os dados transformados
        data_list = []

        for _, row in df.iterrows():
            pais = row['pais']
            for year in years:
                kilos_col = year
                valor_dolar_col = year + '.1'
                kilos = row.get(kilos_col)
                valor_dolar = row.get(valor_dolar_col)
                if pd.notnull(kilos) or pd.notnull(valor_dolar):
                    data = {
                        'pais': pais,
                        'ano': int(year),
                        'kilos': pd.to_numeric(kilos, errors='coerce'),
                        'valor_dolar': pd.to_numeric(valor_dolar, errors='coerce')
                    }
                    data.update(extra_data)
                    data_list.append(data)

        # Criar DataFrame a partir da lista de dados
        df_transformed = pd.DataFrame(data_list)

        # Remover registros onde 'kilos' e 'valor_dolar' são nulos
        df_transformed.dropna(subset=['kilos', 'valor_dolar'], how='all', inplace=True)

        # Inserir os dados no banco de dados
        df_transformed.to_sql(model.__tablename__, con=db.engine, if_exists='append', index=False)
    except Exception as e:
        print(f"Erro ao processar o arquivo {filepath}: {e}")

def sync_data():
    try:
        files = get_file_list()
        if not files:
            print("Sincronização não realizada. Nenhum arquivo disponível.")
            return
        for filename in files:
            remote_mod_time = get_remote_file_mod_time(filename)
            local_filepath = os.path.join(DOWNLOAD_DIR, filename)
            local_mod_time = get_local_file_mod_time(local_filepath)

            # Tentar baixar o arquivo somente se conseguir acessar o remote_mod_time
            if remote_mod_time and (not local_mod_time or remote_mod_time > local_mod_time):
                print(f"Baixando arquivo atualizado: {filename}")
                filepath = download_file(filename)
                if not filepath:
                    print(f"Não foi possível baixar o arquivo: {filename}. Usando arquivo local se disponível.")
                    filepath = local_filepath if os.path.exists(local_filepath) else None
            else:
                print(f"Usando arquivo local para: {filename}")
                filepath = local_filepath if os.path.exists(local_filepath) else None

            if filepath:
                # Aqui vai o processamento dos arquivos conforme seu tipo
                if filename == 'Comercio.csv':
                    Comercializacao.query.delete()
                    db.session.commit()
                    process_csv(filepath, Comercializacao)
                elif filename == 'Producao.csv':
                    Producao.query.delete()
                    db.session.commit()
                    process_csv(filepath, Producao)
                # Continue com os demais arquivos, incluindo os de importação e exportação
                elif filename == 'ImpEspumantes.csv':
                    Importacao.query.filter_by(tipo_produto='Espumante').delete()
                    db.session.commit()
                    process_import_csv(filepath, Importacao, {'tipo_produto': 'Espumante'})
                elif filename == 'ImpFrescas.csv':
                    Importacao.query.filter_by(tipo_produto='Uva Fresca').delete()
                    db.session.commit()
                    process_import_csv(filepath, Importacao, {'tipo_produto': 'Uvas Fresca'})
                elif filename == 'ImpPassas.csv':
                    Importacao.query.filter_by(tipo_produto='Uva Passa').delete()
                    db.session.commit()
                    process_import_csv(filepath, Importacao, {'tipo_produto': 'Uva Passa'})
                elif filename == 'ImpSuco.csv':
                    Importacao.query.filter_by(tipo_produto='Suco').delete()
                    db.session.commit()
                    process_import_csv(filepath, Importacao, {'tipo_produto': 'Suco'})
                elif filename == 'ImpVinhos.csv':
                    Importacao.query.filter_by(tipo_produto='Vinho').delete()
                    db.session.commit()
                    process_import_csv(filepath, Importacao, {'tipo_produto': 'Vinho'})
                
                elif filename == 'ExpEspumantes.csv':
                    Exportacao.query.filter_by(tipo_produto='Espumante').delete()
                    db.session.commit()
                    process_import_csv(filepath, Exportacao, {'tipo_produto': 'Espumante'})
                elif filename == 'ExpSuco.csv':
                    Exportacao.query.filter_by(tipo_produto='Suco').delete()
                    db.session.commit()
                    process_import_csv(filepath, Exportacao, {'tipo_produto': 'Suco'})
                elif filename == 'ExpUva.csv':
                    Exportacao.query.filter_by(tipo_produto='Uva').delete()
                    db.session.commit()
                    process_import_csv(filepath, Exportacao, {'tipo_produto': 'Uva'})
                elif filename == 'ExpVinho.csv':
                    Exportacao.query.filter_by(tipo_produto='Vinho').delete()
                    db.session.commit()
                    process_import_csv(filepath, Exportacao, {'tipo_produto': 'Vinho'})
                    
                # ... Outros arquivos
            else:
                print(f"Arquivo {filename} não disponível localmente. Sincronização deste arquivo não realizada.")
        print("Sincronização de dados concluída.")
    except Exception as e:
        print(f"Erro durante a sincronização de dados: {e}")
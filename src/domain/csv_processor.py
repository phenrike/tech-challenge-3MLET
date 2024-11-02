# src/domain/csv_processor.py
import csv
import pandas as pd
from io import StringIO
from api.models import (TipoImpExp, TipoUva )


class CSVProcessor:

    @staticmethod
    def process_csv_data(csv_content: str, file_type):

        data = []
        imp_files = ["ImpEspumantes.csv", "ImpFrescas.csv", "ImpPassas.csv", "ImpSuco.csv", "ImpVinhos.csv"]
        exp_files = ["ExpEspumantes.csv", "ExpSuco.csv", "ExpUva.csv", "ExpVinho.csv"]
        proc_files = ["ProcessaAmericanas.csv", "ProcessaMesa.csv", "ProcessaSemclass.csv"]
        # coloca nas variaveis a identificacao correspondente ao tipo do arquivo
        if file_type.value == "Producao.csv":
            ds_key = "ds_produto"
            tp_key = "tp_produto"
            dt_key = "dt_ano"
            qt_key = "qt_producao"
            delimiter = ";"
        elif file_type.value == "Comercio.csv":
            ds_key = "ds_produto"
            tp_key = "tp_produto"
            dt_key = "dt_ano"
            qt_key = "qt_comercializacao"
            delimiter = ";"
        elif file_type.value in imp_files:
            ds_key = "ds_pais"
            tp_key = "id_tipo_prod_imp_exp"
            dt_key = "dt_ano"
            qt_key = "qt_importacao"
            vl_key = "vl_importacao"
            delimiter = ";"
        elif file_type.value in exp_files:
            ds_key = "ds_pais"
            tp_key = "id_tipo_prod_imp_exp"
            dt_key = "dt_ano"
            qt_key = "qt_exportacao"
            vl_key = "vl_exportacao"
            delimiter = ";"
        elif file_type.value in proc_files:
            tp_key = "id_tipo_uva"
            ds_key = "ds_cultivo"
            dt_key = "dt_ano"
            qt_key = "qt_processamento"
            delimiter = "\t"
        elif file_type.value == "ProcessaViniferas.csv":
            tp_key = "id_tipo_uva"
            ds_key = "ds_cultivo"
            dt_key = "dt_ano"
            qt_key = "qt_processamento"
            delimiter = ";"

        # Converter o conteúdo do CSV em uma lista de dicionários
        csv_file = StringIO(csv_content)
        # Tente ler o CSV com a codificação correta
        try:
            df = pd.read_csv(csv_file, encoding='utf-8', sep=delimiter)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, encoding='latin1', sep=delimiter)

# Remover espaços no início e fim dos valores em todas as colunas
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # condicao para processar os dados das tabelas de producao e comercializacao
        if file_type.value == "Producao.csv" or file_type.value == "Comercio.csv":
            # transforma os dados de dataframe para dict
            for idx in range(len(df)-1):
                row = df.iloc[idx]
                next_row = df.iloc[idx+1]
                # checa se o valor da linha é todo maiúsculo e associa ao tipo
                if row.iloc[2].isupper():
                    tipo = row.iloc[2]
                    # se o valor da proxima linha for outro tipo, cria um registro para o tipo armazenado
                    if next_row.iloc[2].isupper():
                        for i in range(3, len(row)):
                            data.append({
                                ds_key: row.iloc[2],
                                tp_key: tipo,
                                dt_key: int(df.columns[i]),
                                qt_key: float(row.iloc[i])
                            })
                else:
                    for i in range(3, len(row)):
                        data.append({
                            ds_key: row.iloc[2],
                            tp_key: tipo,
                            dt_key: int(df.columns[i]),
                            qt_key: float(row.iloc[i])
                        })

        # condicao para processar os dados das tabelas de processamento
        elif file_type.value in proc_files or file_type.value == "ProcessaViniferas.csv":
            # checa o id do tipo de arquivo:
            if file_type.value.find('Americanas') != -1:
                tipo_uva = "Americanas e híbridas"
            elif file_type.value.find('Viniferas') != -1:
                tipo_uva = "Viníferas"
            elif file_type.value.find('Mesa') != -1:
                tipo_uva = "Uvas de mesa"
            elif file_type.value.find('Semclass') != -1:
                tipo_uva = "Sem classificação"
                tipo_cultivo = "SEM CLASSIFICAÇÃO"

            tipo_uva_id = TipoUva.query.filter_by(ds_tipo_uva=tipo_uva).first()

            # transforma os dados de dataframe para dict
            for _, row in df.iterrows():
                # checa se o valor da linha é todo maiúsculo e associa ao tipo
                if row.iloc[2].isupper():
                    tipo_cultivo = row.iloc[2]
                else:
                    for i in range(3, len(row)):
                        # tenta transformar o valor para float e retorna None se não for possível (nd e *)
                        try:
                            qt = float(row.iloc[i])
                        except ValueError:
                            qt = None
                        data.append({
                            tp_key: tipo_uva_id.id_tipo_uva,
                            ds_key: tipo_cultivo,
                            dt_key: int(df.columns[i]),
                            qt_key: qt
                        })

        else:
            # checa o id do tipo de arquivo:
            if file_type.value.find('Vinho') != -1:
                tipo = "Vinhos de Mesa"
            elif file_type.value.find('Frescas') != -1 or file_type.value.find('Uva') != -1:
                tipo = "Uvas Frescas"
            elif file_type.value.find('Espumantes') != -1:
                tipo = "Espumantes"
            elif file_type.value.find('Passas') != -1:
                tipo = "Uvas Passas"
            elif file_type.value.find('Suco') != -1:
                tipo = "Suco de Uva"

            tipo_id = TipoImpExp.query.filter_by(ds_tipo_prod_imp_exp=tipo).first()

            # transforma os dados de dataframe para dict
            for _, row in df.iterrows():
                # faz o loop de dois em dois valores para separar as colunas de quantidade e de valor
                for i in range(2, len(row) - 1, 2):
                    data.append({
                        ds_key: row.iloc[1].strip(),
                        tp_key: tipo_id.id_tipo_prod_imp_exp,
                        dt_key: df.columns[i],
                        qt_key: row.iloc[i],
                        vl_key: row.iloc[i+1]
                    })

        return data

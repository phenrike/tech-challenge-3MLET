# src/domain/csv_processor.py
import csv
import pandas as pd
from io import StringIO
from api.models import (TipoImpExp )

class CSVProcessor:

    def parse_csv_with_pandas(csv_content: str) -> pd.DataFrame:
        # Define column names
        columns = ["id", "control", "Produto"] + [str(year) for year in range(1970, 2024)]

        # Load the CSV content into a DataFrame with specified columns
        df = pd.read_csv(StringIO(csv_content), sep=';', header=None, names=columns)

        # Identify wine types and subtypes based on uppercase in 'Produto'
        df['is_type'] = df['Produto'].str.isupper()

        # Forward fill the wine types to group subtypes under them
        df['type'] = df['Produto'].where(df['is_type']).ffill()

        # Separate types and subtypes
        wine_types = df[df['is_type']].copy()
        wine_subtypes = df[~df['is_type']].copy()

        # Merge wine types with their subtypes
        wine_types = wine_types[['id', 'Produto', 'control']].rename(
            columns={"Produto": "type_name", "control": "type_control"})
        merged_data = wine_subtypes.merge(wine_types, how='left', left_on='type', right_on='type_name')

        # Clean up columns for final structure
        merged_data = merged_data.drop(columns=['is_type', 'type_name'])
        merged_data = merged_data.rename(columns={"Produto": "subtype_name", "control": "subtype_control"})

        return merged_data

    @staticmethod
    def process_csv_data(csv_content: str, file_type):

        data = []
        imp_files = ["ImpEspumantes.csv", "ImpFrescas.csv", "ImpPassas.csv", "ImpSuco.csv", "ImpVinhos.csv"]
        exp_files = ["ExpEspumantes.csv", "ExpSuco.csv", "ExpUva.csv", "ExpVinho.csv"]
        # coloca nas variaveis a identificacao correspondente ao tipo do arquivo
        if file_type.value == "Producao.csv":
            control_column = "control"
            product_column = "produto"
            ds_key = "ds_produto"
            tp_key = "tp_produto"
            dt_key = "dt_ano"
            qt_key = "qt_producao"
            delimiter = ";"
        elif file_type.value == "Comercio.csv":
            control_column = "control"
            product_column = "Produto"
            ds_key = "ds_produto"
            tp_key = "tp_produto"
            dt_key = "dt_ano"
            qt_key = "qt_comercializacao"
            delimiter = ";"
        elif file_type.value in imp_files:
            control_column = ""
            ds_key = "ds_pais"
            tp_key = "id_tipo_prod_imp_exp"
            dt_key = "dt_ano"
            qt_key = "qt_importacao"
            vl_key = "vl_importacao"
            delimiter = ";"
        elif file_type.value in exp_files:
            control_column = ""
            ds_key = "ds_pais"
            tp_key = "id_tipo_prod_imp_exp"
            dt_key = "dt_ano"
            qt_key = "qt_exportacao"
            vl_key = "vl_exportacao"
            delimiter = ";"

        # Converter o conteúdo do CSV em uma lista de dicionários
        csv_file = StringIO(csv_content)
        # Tente ler o CSV com a codificação correta
        try:
            df = pd.read_csv(csv_file, encoding='utf-8', sep=delimiter)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, encoding='latin1', sep=delimiter)

        # condicao para processar os dados das tabelas de producao e comercializacao
        if control_column != "":
            # transforma os dados de dataframe para dict
            for idx in range(len(df)-1):
                row = df.iloc[idx]
                next_row = df.iloc[idx+1]
                if row.iloc[2].isupper():
                    tipo = row.iloc[2]
                    if next_row.iloc[2].isupper():
                        for i in range(3, len(row)):
                            data.append({
                                ds_key: row.iloc[2],
                                tp_key: tipo,
                                dt_key: int(df.columns[i]),
                                qt_key: int(row.iloc[i])
                            })
                else:
                    for i in range(3, len(row)):
                        data.append({
                            ds_key: row.iloc[2],
                            tp_key: tipo,
                            dt_key: int(df.columns[i]),
                            qt_key: int(row.iloc[i])
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
                for i in range(2, len(row) - 1, 2):
                    data.append({
                        ds_key: row.iloc[1].strip(),
                        tp_key: tipo_id.id_tipo_prod_imp_exp,
                        dt_key: df.columns[i],
                        qt_key: row.iloc[i],
                        vl_key: row.iloc[i+1]
                    })

        return data

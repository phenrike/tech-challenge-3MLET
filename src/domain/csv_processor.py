# src/domain/csv_processor.py
import csv
import pandas as pd
from io import StringIO
from api.models import (TipoImpExp )

class CSVProcessor:
    
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
            product_column = ""
            country_column = "PaÃ\xads"
            ds_key = "ds_pais"
            tp_key = "id_tipo_prod_imp_exp"
            dt_key = "dt_ano"
            qt_key = "qt_importacao"
            vl_key = "vl_importacao"
            delimiter = ";"
        elif file_type.value in exp_files:
            control_column = ""
            product_column = ""
            country_column = "PaÃ\xads"
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
            for _, row in df.iterrows():
                if row.iloc[2].isupper():
                    tipo = row.iloc[2]
                else:
                    for i in range(3, len(row) - 1):
                        data.append({
                            ds_key: row.iloc[1],
                            tp_key: tipo,
                            dt_key: df.columns[i],
                            qt_key: row.iloc[i]
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

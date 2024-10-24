# src/domain/csv_processor.py
import csv
from io import StringIO

class CSVProcessor:
    
    @staticmethod
    def process_csv_data(csv_content: str, file_type):
        
        data = []
        categoria = ""
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

        # Converter o conteúdo do CSV em uma lista de dicionários
        csv_file = StringIO(csv_content)
        reader = csv.DictReader(csv_file, delimiter=delimiter)

        # lista de colunar que serão ignoradas ao criar o dicionario a partir de pares chave-valor
        skipped_list = ['id', control_column, product_column]
        for row in reader:
            # se for tudo maisculo, indica tipo de produto
            if row[control_column].isupper():
                categoria = row[control_column].title()
            for key, value in row.items():
                # pula os pares em que o valor e maisculo ou nao correspondem a ano e quantidade
                if value in skipped_list or row[product_column].isupper() or key in skipped_list:
                    # skip key value pair
                    ...
                else:
                    data.append({
                        ds_key: row[product_column].strip(),
                        tp_key: categoria,
                        dt_key: key,
                        qt_key: value
                    })
        return data

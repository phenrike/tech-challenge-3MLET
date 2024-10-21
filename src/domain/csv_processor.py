# src/domain/csv_processor.py
import csv
from io import StringIO

class CSVProcessor:
    
    @staticmethod
    def process_csv_data(csv_content: str):
        # Converter o conteúdo do CSV em uma lista de dicionários
        csv_file = StringIO(csv_content)
        reader = csv.DictReader(csv_file,delimiter=';')
        
        data = []
        categoria = ""
        for row in reader:
            if row["control"].isupper():
                categoria = row["control"].title()
            for key, value in row.items():
                # print(key, value)
                if value in ['id', 'control', 'produto'] or row["produto"].isupper() or key in ['id', 'control', 'produto']:
                    # skip key value pair
                    ...
                else:
                    data.append({
                        "ds_produto": row["produto"].strip(),
                        "tp_produto": categoria,
                        "dt_ano": key,
                        "qt_producao": value
                    })
        return data

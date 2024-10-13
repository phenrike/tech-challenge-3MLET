# src/domain/csv_processor.py
import csv
from io import StringIO

class CSVProcessor:
    
    @staticmethod
    def process_csv_data(csv_content: str):
        # Converter o conteúdo do CSV em uma lista de dicionários
        csv_file = StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        data = []
        for row in reader:
            # Processar cada linha do CSV conforme necessário
            data.append({
                "column1": row["Column1"],
                "column2": row["Column2"],
                # Adicionar mais colunas conforme o CSV
            })
        
        return data

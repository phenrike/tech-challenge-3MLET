# src/services/data_ingestion_service.py
from services.csv_factory import CSVFactory
from domain.csv_processor import CSVProcessor
from infra.postgres_repository import PostgresRepository
from api.models import ( Producao , Processamento, Comercializacao, Importacao, Exportacao )
from domain.file_type import FileType

class DataIngestionService:

    @staticmethod
    def process_multiple_csv():
        for file_type in FileType.get_all_files():
            if file_type.value not in ["ProcessaAmericanas.csv","ProcessaMesa.csv", "ProcessaSemclass.csv", "ProcessaViniferas.csv"]:
                # 1. Baixar e processar o CSV
                csv_data = CSVFactory.download_csv_data(file_type)

                # 2. Processar os dados do CSV
                processed_data = CSVProcessor.process_csv_data(csv_data, file_type)

                # 3. Salvar os dados no banco de dados
                #  PostgresRepository.save_data(processed_data)

                if file_type.value == 'Producao.csv':
                    PostgresRepository.save_data(Producao, processed_data)
                elif file_type.value == 'Comercio.csv':
                    PostgresRepository.save_data(Comercializacao, processed_data)
                elif file_type.value.find('Imp') != -1:
                    PostgresRepository.save_data(Importacao, processed_data)
                elif file_type.value.find('Exp') != -1:
                    PostgresRepository.save_data(Exportacao, processed_data)
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
            if file_type.value == 'Producao.csv': # condicao para testar com tabela de producao
                # 1. Baixar e processar o CSV
                csv_data = CSVFactory.download_csv_data(file_type)

                # 2. Processar os dados do CSV
                processed_data = CSVProcessor.process_csv_data(csv_data)

                # 3. Salvar os dados no banco de dados
                #  PostgresRepository.save_data(processed_data)

                PostgresRepository.save_data(Producao, processed_data)

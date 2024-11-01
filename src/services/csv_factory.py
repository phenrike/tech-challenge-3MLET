# src/services/csv_factory.py
from domain.file_type import FileType
from infra.csv_downloader import CSVDownloader

class CSVFactory:
    
    @staticmethod
    def get_csv_url(file_type: FileType) -> str:
        base_url = "http://vitibrasil.cnpuv.embrapa.br/download/"
        #base_url = "http://192.168.3.4:8080/"
        return f"{base_url}{file_type.value}"
    
    @staticmethod
    def download_csv_data(file_type: FileType):
        csv_url = CSVFactory.get_csv_url(file_type)
        csv_data = CSVDownloader.download_csv(csv_url)
        return csv_data

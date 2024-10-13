# src/infra/csv_downloader.py
import requests

class CSVDownloader:
    
    @staticmethod
    def download_csv(url: str) -> str:
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to download CSV from {url}")

        return response.text  # Retorna o conteúdo do CSV como string

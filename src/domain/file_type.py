# src/domain/file_type.py
from enum import Enum

class FileType(Enum):
    COMERCIO = "Comercio.csv"
    EXPESPUMANTES = "ExpEspumantes.csv"
    EXPSUCO = "ExpSuco.csv"
    EXPUVA = "ExpUva.csv"
    EXPVINHO = "ExpVinho.csv"
    IMPESPUMANTES = "ImpEspumantes.csv"
    IMPFRESCAS = "ImpFrescas.csv"
    IMPPASSAS = "ImpPassas.csv"
    IMPSUCO = "ImpSuco.csv"
    IMPVINHOS = "ImpVinhos.csv"
    PROCESSAAMERICANAS = "ProcessaAmericanas.csv"
    PROCESSAMESA = "ProcessaMesa.csv"
    PROCESSASEMCLASS = "ProcessaSemclass.csv"
    PROCESSAVINIFERAS = "ProcessaViniferas.csv"
    PRODUCAO = "Producao.csv"

    @staticmethod
    def get_all_files():
        return [FileType.COMERCIO, FileType.EXPESPUMANTES, FileType.EXPSUCO, FileType.EXPUVA, 
                FileType.EXPVINHO, FileType.IMPESPUMANTES, FileType.IMPFRESCAS, FileType.IMPPASSAS, 
                FileType.IMPSUCO, FileType.IMPVINHOS, FileType.PROCESSAAMERICANAS, FileType.PROCESSAMESA, 
                FileType.PROCESSASEMCLASS, FileType.PROCESSAVINIFERAS, FileType.PRODUCAO]
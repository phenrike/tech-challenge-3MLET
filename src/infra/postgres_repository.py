# src/infra/postgres_repository.py
import psycopg2
from infra.db_connection import get_db_connection

class PostgresRepository:
    
    @staticmethod
    def save_data(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for row in data:
            cursor.execute("""
                INSERT INTO my_table (column1, column2)
                VALUES (%s, %s)
            """, (row["column1"], row["column2"]))
        
        conn.commit()
        cursor.close()
        conn.close()

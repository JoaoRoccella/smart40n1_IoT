import os
from mysql.connector import Error
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                passwd=os.getenv("DB_PASWD"),
                database=os.getenv("DB_NAME")
            )
            print("Conexão com o MySQL realizada com sucesso")
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Conexão com o MySQL encerrada")

    def execute_query(self, query, params=None):
        with self as conn:
            if conn is None:
                return None
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                if query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result
                else:
                    conn.commit()
                    return cursor.rowcount
            except Error as e:
                print(f"Erro ao executar a query: {e}")
                return None
            finally:
                cursor.close()
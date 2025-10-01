import mysql.connector as mc
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Any, Tuple, List

class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.host = getenv('DB_HOST')
        self.username = getenv('DB_USER')
        self.password = getenv('DB_PSWD')
        self.database = getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None
        
    def __enter__(self) -> 'Database':
        self.conectar()
        return self
    
    def __exit__(self, exc_type: Optional[Any], exc_value: Optional[Any], exc_traceback: Optional[Any]) -> None:
        self.desconectar()
        if exc_type is not None:
            print(f"Ocorreu um erro: {exc_value}")

    def conectar(self) -> None:
        try:
            self.connection = mc.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                print("Conectou ao banco de dados com sucesso.")

        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.connection = None
            raise e

    def desconectar(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Desconectou do banco de dados.")

    def executar_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[dict]]:
        if not self.connection or not self.connection.is_connected():
            raise Exception("Conexão com o banco de dados não está ativa.")
        
        cursor: Optional[MySQLCursorDict] = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            # Retorna resultados apenas para SELECTs
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            
            else:
                self.connection.commit()
                
                # Retorna o ID do último registro inserido para INSERTs
                if query.strip().upper().startswith("INSERT"):
                    return cursor.lastrowid
                
                return cursor.rowcount # Para UPDATE/DELETE
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()


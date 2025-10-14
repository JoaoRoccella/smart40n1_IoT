import os
import sqlite3
import mysql.connector as mc
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict
from dotenv import load_dotenv
from typing import Optional, Any, Tuple, List
from pathlib import Path


# ======================
# === MYSQL DATABASE ===
# ======================

class DatabaseMySQL:
    def __init__(self) -> None:
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PSWD')
        self.database = os.getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None
        
    def __enter__(self) -> 'DatabaseMySQL':
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
                database=self.database,
                port=int(os.getenv("DB_PORT", 3306))
            )
            
            if self.connection.is_connected():
                print(f"[MySQL] Conectou ao banco {self.database} com sucesso.")

        except Exception as e:
            print(f"Erro ao conectar ao banco MySQL: {e}")
            self.connection = None
            raise e

    def desconectar(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("[MySQL] Desconectou do banco de dados.")

    def executar_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[dict]]:
        if not self.connection or not self.connection.is_connected():
            raise Exception("Conexão MySQL não está ativa.")
        
        cursor: Optional[MySQLCursorDict] = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.connection.commit()
                if query.strip().upper().startswith("INSERT"):
                    return cursor.lastrowid
                return cursor.rowcount
        except Exception as e:
            print(f"[MySQL] Erro ao executar a query: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()


# =======================
# === SQLITE DATABASE ===
# =======================

class DatabaseSQLite:
    def __init__(self) -> None:
        load_dotenv()
        db_name = os.getenv("DB_NAME", "database")
        self.database = os.path.join("data", f"{db_name}.db")
        self.db_path = Path(self.database).resolve()
        self.connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> 'DatabaseSQLite':
        self.conectar()
        return self
    
    def __exit__(self, exc_type: Optional[Any], exc_value: Optional[Any], exc_traceback: Optional[Any]) -> None:
        self.desconectar()
        if exc_type is not None:
            print(f"Ocorreu um erro: {exc_value}")

    def conectar(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print(f"[SQLite] Conectou ao banco em {self.db_path}")
        except Exception as e:
            print(f"Erro ao conectar ao banco SQLite: {e}")
            raise e

    def desconectar(self) -> None:
        if self.connection:
            self.connection.close()
            print("[SQLite] Desconectou do banco de dados.")

    def executar_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[dict]]:
        if not self.connection:
            raise Exception("Conexão SQLite não está ativa.")
        
        cursor: Optional[sqlite3.Cursor] = None
        try:
            cursor = self.connection.cursor()
            query = query.replace("%s", "?")  # compatibilidade com MySQL
            cursor.execute(query, params or ())

            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            elif query.strip().upper().startswith("INSERT"):
                self.connection.commit()
                return cursor.lastrowid
            else:
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"[SQLite] Erro ao executar a query: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()

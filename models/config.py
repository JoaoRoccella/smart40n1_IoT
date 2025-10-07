import os
from dotenv import load_dotenv
from models.database import DatabaseMySQL, DatabaseSQLite

load_dotenv()

# Define tipo do banco no .env: DB_TYPE=mysql ou DB_TYPE=sqlite
db_type = os.getenv("DB_TYPE", "sqlite").lower()

if db_type == "mysql":
    Database = DatabaseMySQL
    print("[CONFIG] Usando banco de dados MySQL")
elif db_type == "sqlite":
    Database = DatabaseSQLite
    print("[CONFIG] Usando banco de dados SQLite")
else:
    raise ValueError(f"Tipo de banco de dados desconhecido: {db_type}")

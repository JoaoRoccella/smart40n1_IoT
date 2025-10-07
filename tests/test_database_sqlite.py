import pytest
from models.database import DatabaseSQLite

@pytest.fixture
def db_temp(tmp_path):
    # cria o banco temporário
    db = DatabaseSQLite()
    db.db_path = str(tmp_path / "test.db")
    db.conectar()

    # cria as tabelas com base no schema.sql
    with open("data/schema.sql", "r", encoding="utf-8") as f:
        schema = f.read()

    # acessa o cursor diretamente pela conexão
    cursor = db.connection.cursor()
    cursor.executescript(schema)
    db.connection.commit()

    yield db
    db.desconectar()


def test_buscar_ultima_variavel(db_temp):
    # insere dado de exemplo
    db_temp.executar_query(
        "INSERT INTO data (variable, value) VALUES (?, ?)",
        ("temperatura", 25.4)
    )

    query = "SELECT variable, value FROM data WHERE variable = ?"
    result = db_temp.executar_query(query, ("temperatura",))

    assert result[0]["variable"] == "temperatura"
    assert float(result[0]["value"]) == 25.4  # garante conversão numérica
    assert len(result) == 1

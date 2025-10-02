import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.mqtt_handler import connect_mqtt, subscribe
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    client = connect_mqtt()
    topic = os.getenv("MQTT_TPIC", "#")
    subscribe(client, topic)

    client.loop_start()  # inicia thread do Paho para receber mensagens
    app.state.mqtt_client = client  # garante que o client não seja destruído
    print("[APP] MQTT conectado e loop iniciado.")

    yield  # libera app para atender rotas

    # --- Shutdown ---
    client.loop_stop()
    client.disconnect()
    print("[APP] MQTT desconectado.")


app = FastAPI(lifespan=lifespan)


@app.get("/helloThere")
def ping():
    return {"line": "General Kenobi!"}


@app.get("/{variable}/last")
@app.get("/{variable}/last/{time}/{unit}")
def get_last_variable(variable: str, time: Optional[str] = None, unit: Optional[str]= None):
    from models.database import Database

    # mapeamento para unidades MySQL (sempre em singular)
    units_allowed = {
        "minutes": "MINUTE", "minute": "MINUTE", 
        "hours": "HOUR", "hour": "HOUR", 
        "days": "DAY", "day": "DAY"
    }

    # validação inicial
    if time and unit:  # caso exista intervalo
        if not (time.isdigit() and unit.lower() in units_allowed):
            return {"erro": "Parâmetros inválidos."}


    # Query base
    query = "SELECT `variable`, `value`, `timestamp` FROM `data` WHERE `variable` = %s"

    if time and unit:  # intervalo
        unit_sql = units_allowed[unit.lower()]
        query += f" AND `timestamp` >= NOW() - INTERVAL {int(time)} {unit_sql} ORDER BY `timestamp` DESC"
    else:  # último registro
        query += " ORDER BY `timestamp` DESC LIMIT 1"
    

    try:
        with Database() as db:
            result = db.executar_query(query, (variable,))
            if result:
                return result
            else:
                return {
                    "mensagem": f"Nenhum registro de {variable} foi encontrado.",
                    "query": query, "params": (variable,)}
    except Exception as e:
        return {"erro": str(e), "query": query}



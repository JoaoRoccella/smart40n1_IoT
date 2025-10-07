import os
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from services.mqtt_handler import connect_mqtt, subscribe
from models.payload import LastVariablePayload


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = connect_mqtt()
    topic = os.getenv("MQTT_TPIC", "#")
    subscribe(client, topic)
    client.loop_start()
    app.state.mqtt_client = client
    print("[APP] MQTT conectado e loop iniciado.")

    yield

    client.loop_stop()
    client.disconnect()
    print("[APP] MQTT desconectado.")


app = FastAPI(lifespan=lifespan)


@app.get("/helloThere")
def ping():
    return {"line": "General Kenobi!"}


@app.get("/{variable}/last")
@app.get("/{variable}/last/{time}/{unit}")
def get_last_variable(payload: LastVariablePayload = Depends()):
    """
    Endpoint delega toda a validação e execução da query ao payload.py.
    """
    return payload.fetch()

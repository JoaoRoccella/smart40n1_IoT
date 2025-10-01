import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.mqtt_handler import connect_mqtt, subscribe

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


@app.get("/ping")
def ping():
    return {"status": "ok"}

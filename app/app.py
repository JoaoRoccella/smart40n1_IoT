import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.mqtt_handler import connect_mqtt, subscribe
from routes import general, smart40n1

# Define o lifespan para gerenciar a conexão MQTT
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

app.title = "API para Bancada Smart4.0 N1"
app.version = "1.0.0"
app.description = """
API desenvolvida para gerenciar e armazenar dados da Bancada Smart4.0 N1. 
Utiliza MQTT para comunicação segura e FastAPI para endpoints RESTful.
"""
app.terms_of_service = "http://example.com/terms/"
app.contact = {
    "name": "Suporte Smart4.0 N1",
    "url": "http://example.com/contact/",
    "email": "joao.a@docente.senai.br",
}

app.include_router(general.router)
app.include_router(smart40n1.router)

import os
import json
import logging
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from models.database import Database

load_dotenv()

# Configuração global de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
)
logger = logging.getLogger("mqtt_logger")


def connect_mqtt() -> mqtt.Client:
    """Conecta ao broker MQTT com TLS/SSL."""
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PSWD"))

    # Habilita TLS
    client.tls_set()  # usa certificados CA default do sistema

    client.connect(os.getenv("MQTT_BRKR"), int(os.getenv("MQTT_PORT")))
    logger.info("Cliente MQTT conectado ao broker via TLS")
    return client


def insert_message_to_db(topic: str, variable: str, value: str):
    """Insere uma mensagem recebida no banco de dados."""
    
    query = "INSERT INTO `data` (`topic`,`variable`, `value`) VALUES (%s, %s, %s);"
    params = (topic, variable, value)

    try:
        with Database() as db:
            db.executar_query(query, params)
            logger.info(f"Mensagem inserida na database: topic={topic}, variable={variable}, value={value}")
    except Exception as e:
        logger.error(f"Erro ao inserir mensagem na database: {e}")


def subscribe(client: mqtt.Client, topic: str):
    """Inscreve no tópico e define callback de mensagem."""

    def on_message(client_inner, userdata, msg):
        logger.info(f"Mensagem recebida em {msg.topic}: {msg.payload.decode()}")
        
        try:
            topic = msg.topic
            data = json.loads(msg.payload.decode())
            variable = data.get("variable")
            value = data.get("value")
            if variable is not None and value is not None:
                insert_message_to_db(topic, variable, value)
            else:
                logger.warning("Mensagem JSON não contém as chaves esperadas")
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON da mensagem: {e}")
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")

    client.on_message = on_message  # atribuição antes do subscribe
    client.subscribe(topic)
    logger.info(f"Inscrito no tópico MQTT: {topic}")

    return client

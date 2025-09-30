import paho.mqtt.client as mqtt
import os
import json
from dotenv import load_dotenv
from models.database import MySQLConnection

load_dotenv()

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PSWD"))
    client.connect(os.getenv("MQTT_BRKR"), int(os.getenv("MQTT_PORT")))
    return client

def insert_message_to_db(variable, value):
    query = "INSERT INTO `data` (`variable`, `value`) VALUES (%s, %s)"
    params = (variable, value)
    with MySQLConnection() as db:
        if db is not None:
            cursor = db.cursor()
            try:
                cursor.execute(query, params)
                db.commit()
                print(f"Mensagem inserida no banco: variable={variable}, value={value}")
            except Exception as e:
                print(f"Erro ao inserir mensagem no banco: {e}")
            finally:
                cursor.close()
        else:
            print("Não foi possível conectar ao banco de dados.")

def subscribe(client: mqtt.Client, topic: str):
    def on_message(client, userdata, msg):
        print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
        try:
            data = json.loads(msg.payload.decode())
            variable = data.get("variable")
            value = data.get("value")
            if variable is not None and value is not None:
                insert_message_to_db(variable, value)
            else:
                print("Mensagem JSON não contém as chaves esperadas.")
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    client.subscribe(topic)
    client.on_message = on_message
    print(f"Inscrito no tópico: {topic}")
    return client

def run():
    client = connect_mqtt()
    topic = os.getenv("MQTT_TPIC", "#")
    client = subscribe(client, topic)
    client.loop_forever()
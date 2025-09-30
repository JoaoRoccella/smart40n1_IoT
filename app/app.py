from fastapi import FastAPI
import threading
from models import mqtt_connect
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=mqtt_connect.run, daemon=True)
    thread.start()
    yield

app = FastAPI(lifespan=lifespan)
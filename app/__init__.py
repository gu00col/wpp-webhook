from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from dotenv import load_dotenv
import os
from os.path import isfile, join
import sys
import threading

# Configuração do Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

env_path = 'app/.env'

if isfile(env_path):
    # Carregamentos de variáveis env
    load_dotenv(env_path)
    global_api_key = os.getenv('global_api_key')
    baileys_host = os.getenv('baileys_host')
else:
    logger.error('ENV INVALIDA.')
    sys.exit(1)


app = FastAPI()


from app.rotas.webhook import router as webhook
app.include_router(webhook)

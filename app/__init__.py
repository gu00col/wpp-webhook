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

from app.funcoes.evolution_api import feet_all_instances, adiciona_numero_contatos, atualiza_fotos_contatos

scheduler_lock = threading.Lock()

def start_scheduler():
    with scheduler_lock:
        if not scheduler.running:
            logger.info("Scheduler start")
            # scheduler.add_job(atualiza_fotos_contatos, 'interval', minutes=5)  # Executa a cada 1 minuto
            scheduler.start()
            logger.info("Scheduler started successfully")

# Configuração do APScheduler
scheduler = BackgroundScheduler()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    logger.info("Scheduler shut down successfully")

from app.rotas.webhook import router as webhook
app.include_router(webhook)

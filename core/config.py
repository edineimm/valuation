import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

ENV = os.getenv("ENV", "DEV")

CSV_INDEX_PATH = os.getenv("CSV_INDEX_PATH")
CSV_TICKETS_PATH = os.getenv("CSV_TICKETS_PATH")
FOLDER = os.getenv("FOLDER")

LOG_PATH = os.getenv("LOG_PATH", "logs/")

ANO = int(os.getenv("ANO", "1"))
KE = float(os.getenv("KE", "1.0"))
TOP_COMPANIES = int(os.getenv("TOP_COMPANIES", "1"))

MAX_RETRY = int(os.getenv("MAX_RETRY", "1"))
THREAD_WORKERS = int(os.getenv("THREAD_WORKERS", "1"))

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
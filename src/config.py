# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:57:45 2026

@author: bbrave
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Diretório principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretórios de dados
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Carrega variáveis do arquivo .env
load_dotenv(BASE_DIR / ".env")

# Configuração do PostgreSQL
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
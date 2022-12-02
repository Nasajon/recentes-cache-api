import os
import logging
import sys
import time
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS

# Lendo variáveis de ambiente
load_dotenv()

APP_NAME = os.environ['APP_NAME']
DEBUG = os.getenv('DEBUG', 'False') == 'True'
MOPE_CODE = os.environ['MOPE_CODE']

CONTENT_TYPE_JSON_HEADER = {'Content-Type' : 'application/json'}

IGNORE_AUTH = os.getenv('IGNORE_AUTH', 'False') == 'True'

SERVER_PORT = os.getenv('SERVER_PORT', 5000)

MAX_HISTORICS = os.getenv('MAX_HISTORICS', 10)

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

EXPIRATION_SECONDS = os.getenv('EXPIRATION_SECONDS', 60)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

OAUTH_CLIENT_ID = os.environ['OAUTH_CLIENT_ID']
OAUTH_CLIENT_SECRET = os.environ['OAUTH_CLIENT_SECRET']
OAUTH_TOKEN_INTROSPECTION_URL = os.environ['OAUTH_TOKEN_INTROSPECTION_URL']

APIKEY_VALIDATE_URL = os.getenv('APIKEY_VALIDATE_URL')


# Keycloak
PROFILE_ENDPOINT=os.getenv('PROFILE_ENDPOINT')

# Diretório
DIRETORIO_ENDPOINT=os.getenv('DIRETORIO_ENDPOINT')
API_KEY=os.getenv('API_KEY')




# Configurando o logger
logger = logging.getLogger(APP_NAME)
if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)

console_format = logging.Formatter(
    '%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

logger.addHandler(console_handler)


def log_time(msg: str):
    """Decorator para monitoria de performance de métodos (via log)."""

    def decorator(function):
        def wrapper(*arg, **kwargs):
            t = time.time()
            res = function(*arg, **kwargs)
            logger.info(f'----- {str(time.time()-t)} seconds --- {msg}')
            return res

        return wrapper

# Importando e abrindo ouvinte para conexão remota
# ptvsd.enable_attach(("0.0.0.0", 5678))

# Configurando o Flask
application = Flask('app')
CORS(application)
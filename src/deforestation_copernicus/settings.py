import os

SERVICE_NAME = 'deforestation_copernicus'
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA = os.path.join(ROOT, 'data')

COPPERNICUS_CLIENT_ID = os.getenv('COPPERNICUS_CLIENT_ID')
COPPERNICUS_CLIENT_SECRET = os.getenv('COPPERNICUS_CLIENT_SECRET')

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')



DEBUG = int(os.getenv('DEBUG', '0'))
LOGGER_PATH = os.getenv('LOGGER_PATH')

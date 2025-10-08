import os

from typing import Literal


SERVICE_NAME = 'deforestation_copernicus'
try:
    __VERSION__ = open('/app/__version__').readline().strip()
except Exception as _:
    __VERSION__ = None
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

KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS = 'satellite-download-requests'
KAFKA_TOPIC__SATELLITE_TO_DOWNLOAD = 'satellite-to-download'

# we could create and use access keys, but for now we keep it like this
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')


MINIO_HOST = os.getenv('MINIO_HOST')
MINIO_S3_PORT = os.getenv('MINIO_S3_PORT')
MINIO_ENDPOINT = f"{MINIO_HOST}:{MINIO_S3_PORT}"
KAFKA_BROKER = os.getenv('KAFKA_BROKER')



DELTA_TABLES_NAME = os.getenv('DELTA_TABLES_NAME')
SATELLITE_DATA_BUCKET = os.getenv('SATELLITE_DATA_BUCKET')
SENSOR_DATA_BUCKET = os.getenv('SENSOR_DATA_BUCKET')
SATELLITE_PARTITION_KEY = os.getenv('SATELLITE_PARTITION_KEY')




STORAGE_OPTIONS = {
        "AWS_ACCESS_KEY_ID": MINIO_ROOT_USER,
        "AWS_SECRET_ACCESS_KEY": MINIO_ROOT_PASSWORD,
        "AWS_ENDPOINT_URL": f"http://{MINIO_ENDPOINT}",
        "AWS_ALLOW_HTTP": "true",
    }
# TIMEOUT TO RESTART READING MESSAGES
CONSUMER_TIMEOUT_MS = 1000
KAFKA_PUSH_BATCH_SIZE = 10_000
MONGO_BATCH_SIZE = 50_000
CONSUMER_BATCH_SIZE = int(os.getenv('CONSUMER_BATCH_SIZE'))


PARTITION_GEOHASH_LEVEL = int(os.getenv('PARTITION_GEOHASH_LEVEL', '3'))


SATELLITE_PARTITION_KEY = 'geohash'
SATELLITE_UPSERT_KEYS = ['srid', 'timestamp_start', 'timestamp_end', 'geohash']



MINIO_WRITE_RETRIES = int(os.getenv('MINIO_WRITE_RETRIES', '5'))
MINIO_WRITE_RETRY_DELAY = int(os.getenv('MINIO_WRITE_RETRY_DELAY', '1'))
MINIO_WRITE_RETRY_BACKOFF = int(os.getenv('MINIO_WRITE_RETRY_BACKOFF', '2'))


IMAGE_NAME_TIFF = 'image.tiff'
IMAGE_NAME_COG = 'image.cog'
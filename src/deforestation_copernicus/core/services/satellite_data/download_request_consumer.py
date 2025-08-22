from datetime import datetime, timezone
from deltalake import DeltaTable, write_deltalake


import polars
from deforestation_copernicus.io.sentinel_hub.universal_fetcher import SentinelHubFetcher
from deforestation_copernicus.core.data_models.satellite_data import SatelliteData
from deforestation_copernicus.core.data_models.download_request import DownloadRequest
from deforestation_copernicus.io.kafka.base_consumer import BaseConsumer
from deforestation_copernicus.io.kafka.base_producer import BaseProducer
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.io.minio.client_minio import ClientMinio
from deforestation_copernicus.core.utils.utils import get_table_delta_uri
from deforestation_copernicus.settings import KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS, KAFKA_TOPIC__SATELLITE_TO_DOWNLOAD, CONSUMER_TIMEOUT_MS, CONSUMER_BATCH_SIZE, SATELLITE_DATA_BUCKET, DELTA_TABLES_NAME, STORAGE_OPTIONS, SATELLITE_PARTITION_KEY, SATELLITE_UPSERT_KEYS, IMAGE_NAME_TIFF
import tempfile
from deforestation_copernicus.core.utils.config import CoppernicusConfig


class DownloadRequestConsumer():
    group_id = 'download_request_consumer'
    def __init__(self):
        self.client_consumer = BaseConsumer(topics=[KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS],
                                            consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
                                            group_id=self.group_id)
        self.client_minio = ClientMinio(bucket_name=SATELLITE_DATA_BUCKET)

    def run(self):
        batch = []
        for msg in self.client_consumer.consumer:
            batch.append(SatelliteData(**msg.value))
            if len(batch) >= CONSUMER_BATCH_SIZE:
                break
        if not batch:
            return
        to_download = []
        satellite_data: SatelliteData
        for satellite_data in batch:
            if not self.client_minio.get_objects(satellite_data.get_minio_path()):
                to_download.append(DownloadRequest.from_dict(satellite_data.to_dict()))
        if not to_download:
            return
        kafka_producer = BaseProducer()
        for request in to_download:
            kafka_producer.producer.send(topic=KAFKA_TOPIC__SATELLITE_TO_DOWNLOAD,
                                         value=request.to_dict())
        kafka_producer.producer.flush()
        logger.debug(f'Pushed {len(to_download)} download requests to Kafka:{KAFKA_TOPIC__SATELLITE_TO_DOWNLOAD}')

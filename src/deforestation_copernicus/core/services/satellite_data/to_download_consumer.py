from datetime import datetime, timezone
from deltalake import DeltaTable, write_deltalake

import polars
from deforestation_copernicus.io.sentinel_hub.universal_fetcher import SentinelHubFetcher
from deforestation_copernicus.core.data_models.satellite_data import SatelliteData
from deforestation_copernicus.core.data_models.download_request import DownloadRequest
from deforestation_copernicus.core.data_models.sentinel_hub_result import SentinelHubResult
from deforestation_copernicus.io.kafka.base_consumer import BaseConsumer
from deforestation_copernicus.io.kafka.base_producer import BaseProducer

from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.io.minio.client_minio import ClientMinio
from deforestation_copernicus.core.utils.utils import get_table_delta_uri, create_cog
from deforestation_copernicus.settings import KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS, KAFKA_TOPIC__SATELLITE_TO_DOWNLOAD, CONSUMER_TIMEOUT_MS, CONSUMER_BATCH_SIZE, SATELLITE_DATA_BUCKET, DELTA_TABLES_NAME, STORAGE_OPTIONS, SATELLITE_PARTITION_KEY, SATELLITE_UPSERT_KEYS, IMAGE_NAME_TIFF
import tempfile
from deforestation_copernicus.core.utils.config import CoppernicusConfig
import os
from typing import Iterable

class ToDownloadConsumer():
    group_id = 'to_download_consumer'
    def __init__(self):
        self.client_consumer = BaseConsumer(topics=[KAFKA_TOPIC__SATELLITE_TO_DOWNLOAD],
                                            consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
                                            group_id=self.group_id)
        self.client_minio = ClientMinio(bucket_name=SATELLITE_DATA_BUCKET)

    def download_data(self, list_satellite_data: list[SatelliteData], data_folder: str) -> Iterable[SentinelHubResult]:
        config = CoppernicusConfig()
        fetcher = SentinelHubFetcher(config=config, data_folder=data_folder)
        # TODO finish this, we need to download the data and then write to minio.
        # not sure if we need sentinel hub results now, probably only in the postgis syncer
        for satellite_data in list_satellite_data:
            for sentinel_hub_result in fetcher.run(satellite_data=satellite_data):
                yield sentinel_hub_result


    def run(self):
        '''checks deltable for already downloaded data. if it exists, it double checks minio for these paths
        otherwise it downloads the data and pushes to minio and then upserts/inserts entry into deltatable'''
        # delta_table_uri = get_table_delta_uri(delta_bucket=SATELLITE_DATA_BUCKET,
        #                                       delta_table=DELTA_TABLES_NAME)
        # data_folder = tempfile.TemporaryDirectory().name
        data_folder = '/home/pedroq/workspace/deforestation_copernicus/data/'
        batch = []
        for msg in self.client_consumer.consumer:
            batch.append(SatelliteData(**msg.value))
            if len(batch) >= CONSUMER_BATCH_SIZE:
                break
        if not batch:
            return
        sentinel_hub_result: SentinelHubResult
        for sentinel_hub_result in self.download_data(list_satellite_data=batch, data_folder=data_folder):
            print(sentinel_hub_result)
            local_tiff_path = os.path.join(data_folder, sentinel_hub_result.image_type, sentinel_hub_result.srid, 'response.tiff')
            local_cog_path = os.path.join(data_folder, sentinel_hub_result.image_type, sentinel_hub_result.srid, 'response.cog')
            cog_metadata = {
                'srid': sentinel_hub_result.srid,
                'resolution': sentinel_hub_result.resolution,
                'timestamp_start': sentinel_hub_result.timestamp_start.isoformat(),
                'timestamp_end': sentinel_hub_result.timestamp_end.isoformat(),
                'image_type': sentinel_hub_result.image_type,
                }
            create_cog(input_path=local_tiff_path, output_path=local_cog_path,additional_cog_metadata=cog_metadata)
            logger.debug(f'Created cog {local_cog_path}')
            


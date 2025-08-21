from deforestation_copernicus.core.data_models.download_request import DownloadRequest
from deforestation_copernicus.io.base_kafka_producer import BaseProducer
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.settings import KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS


class DownloadRequestPusher():

    @staticmethod
    def run(download_requests: list[DownloadRequest]):
        kafka_producer = BaseProducer()
        for request in download_requests:
            kafka_producer.producer.send(topic=KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS,
                                         value=request.to_dict())
        kafka_producer.producer.flush()
        logger.debug(f'Pushed {len(download_requests)} download requests to Kafka:{KAFKA_TOPIC__SATELLITE_DOWNLOAD_REQUESTS}')

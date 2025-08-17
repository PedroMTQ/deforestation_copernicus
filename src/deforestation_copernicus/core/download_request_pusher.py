from datetime import datetime, timezone

from faker import Faker

from deforestation_copernicus.core.messages.download_request import DownloadRequestBoundingBoxWGS84
from deforestation_copernicus.io.base_kafka_producer import BaseProducer
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.settings import KAFKA_TOPIC__DOWNLOAD_REQUESTS


FAKE_DATA_GENERATOR = Faker()


class DownloadRequestPusher():

    @staticmethod
    def run(download_requests: list[DownloadRequestBoundingBoxWGS84]):
        kafka_producer = BaseProducer()
        for request in download_requests:
            kafka_producer.producer.send(topic=KAFKA_TOPIC__DOWNLOAD_REQUESTS,
                                         value=request.to_dict())
        kafka_producer.producer.flush()

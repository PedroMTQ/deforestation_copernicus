from kafka import KafkaProducer

from deforestation_copernicus.core.utils.utils import serializer
from deforestation_copernicus.settings import KAFKA_BROKER


class BaseProducer(KafkaProducer):
    def __init__(self):
        if not KAFKA_BROKER:
            raise Exception('Missing KAFKA_BROKER')
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                                      value_serializer=serializer)

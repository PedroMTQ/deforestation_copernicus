from abc import abstractmethod
from typing import Optional
from kafka_deltalake_minio.io.logger import logger

from kafka import KafkaConsumer

from kafka_deltalake_minio.core.utils import deserializer
from kafka_deltalake_minio.settings import KAFKA_BROKER


class BaseConsumer(KafkaConsumer):
    def __init__(self,
                 topics: list[str],
                 consumer_timeout_ms: int,
                 group_id: Optional[str]=None):
        if not KAFKA_BROKER:
            raise Exception('Missing KAFKA_BROKER')
        self.topics = topics
        self.group_id = group_id
        self.consumer = KafkaConsumer(bootstrap_servers=KAFKA_BROKER,
                                      group_id=self.group_id,
                                      value_deserializer=deserializer,
                                      consumer_timeout_ms=consumer_timeout_ms,
                                  )
        self.consumer.subscribe(self.topics)
        logger.info(self)

    def __str__(self):
        return f'{self.__class__.__name__} from group <{self.group_id}> is consuming from {self.topics} at {KAFKA_BROKER}'

    @abstractmethod
    def run(self):
        return

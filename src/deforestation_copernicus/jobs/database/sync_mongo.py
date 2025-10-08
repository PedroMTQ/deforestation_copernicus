import time

from kafka_deltalake_minio.core.mongo_syncer import MongoSyncer
from kafka_deltalake_minio.io.logger import logger
from kafka_deltalake_minio.settings import (
    MONGO_SYNC_SLEEP_TIME,
)


class SyncMongoJob():
    def start_service(self):
        while True:
            mongo_syncer = MongoSyncer()
            try:
                mongo_syncer.run()
            except Exception as e:
                logger.exception(f'Failed to sync mongo due to {e}')
            logger.info(f'Sleeping for {MONGO_SYNC_SLEEP_TIME} seconds')
            time.sleep(MONGO_SYNC_SLEEP_TIME)


if __name__ == '__main__':
    test = SyncMongoJob()
    test.start_service()

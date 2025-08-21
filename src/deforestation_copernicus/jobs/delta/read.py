from kafka_deltalake_minio.io.delta_table_reader import DeltaTableReader
from kafka_deltalake_minio.io.logger import logger


class ReadJob():
    @staticmethod
    def run(list_ids: list[int]):
        for customer_id in list_ids:
            customer_data = DeltaTableReader.get_customer_data(customer_id=customer_id)
            if len(customer_data) > 1:
                logger.error(f'Found too many rows for {customer_id}')
            print(customer_data)


if __name__ == '__main__':
    list_ids = [1]
    job = ReadJob.run(list_ids=list_ids)

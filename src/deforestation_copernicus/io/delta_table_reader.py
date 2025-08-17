import polars
from deforestation_copernicus.core.utils.utils import get_table_delta_uri
from deforestation_copernicus.settings import STORAGE_OPTIONS
from datetime import datetime
from kafka_deltalake_minio.core.customer_data import CustomerData
from kafka_deltalake_minio.io.logger import logger

class DeltaTableReader():

    @staticmethod
    def get_customer_data(customer_id: int, version: int=None, timestamp: datetime=None) -> list[CustomerData]:
        try:
            lazy_frame: polars.LazyFrame = polars.scan_delta(source=DELTA_TABLE_URI, storage_options=STORAGE_OPTIONS, version=version or timestamp)
        except Exception as _:
            logger.warning(f'{DELTA_TABLE_URI} not found...')
            return []
        data  = lazy_frame.filter(polars.col('_id') == customer_id).collect()
        return [CustomerData(**row) for row in data.to_dicts()]

if __name__ == '__main__':
    # job = PopulateMongo.run(n_customers=1_000_000_000)
    data = DeltaTableReader.get_customer_data(customer_id=1)
    for i in data:
        print(i)
    # job = PopulateMongo.run(n_customers=1)


import polars
from deltalake import DeltaTable, write_deltalake

from deforestation_copernicus.core.utils.utils import get_table_delta_uri
from deforestation_copernicus.io.base_kafka_consumer import BaseConsumer
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.settings import (
    CONSUMER_BATCH_SIZE,
    CONSUMER_TIMEOUT_MS,
    STORAGE_OPTIONS,
)
from deforestation_copernicus.settings import STORAGE_OPTIONS


class KafkaToDeltaConsumer(BaseConsumer):
    group_id = 'delta'
    def __init__(self):
        super().__init__(topics=[KAFKA_TOPIC],
                         consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
                         group_id=self.group_id)

    def run(self):
        batch = []
        for msg in self.consumer:
            batch.append(msg.value)
            if len(batch) >= CONSUMER_BATCH_SIZE:
                break
        if not batch:
            return
        if not DeltaTable.is_deltatable(DELTA_TABLE_URI, storage_options=STORAGE_OPTIONS):
            new_table = polars.DataFrame(batch)
            write_deltalake(DELTA_TABLE_URI,
                            data=new_table,
                            storage_options=STORAGE_OPTIONS,
                            partition_by=PARTITION_KEY)
            logger.info(f'Wrote new table {DELTA_TABLE_URI}')
            return
        dt = DeltaTable(DELTA_TABLE_URI, storage_options=STORAGE_OPTIONS)
        update_df = polars.DataFrame(batch)
        # we dont use when_matched_update_all in case the schema updates over time
        update_keys = (k for k in update_df.columns  if k != UPSERT_KEY)
        update_command = {k: f'source.{k}' for k in update_keys}
        dt.merge(source=update_df,
                 predicate=f"target.{UPSERT_KEY} = source.{UPSERT_KEY} AND target.{PARTITION_KEY} = source.{PARTITION_KEY}",
                 source_alias="source",
                 target_alias="target"
                 ).when_matched_update(updates=update_command
                 ).when_not_matched_insert_all(
                 ).execute()
        logger.info(f"Wrote {len(batch)} records to Delta table")


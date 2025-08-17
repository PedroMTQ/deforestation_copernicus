import polars
from deltalake import DeltaTable

from deforestation_copernicus.core.utils.utils import get_table_delta_uri
from deforestation_copernicus.settings import STORAGE_OPTIONS

class ReadChangesJob():

    @staticmethod
    def run():
        try:
            dt = DeltaTable(DELTA_TABLE_URI, storage_options=STORAGE_OPTIONS)
            table = dt.load_cdf(starting_version=1, ending_version=dt.version()).read_all()
            pt = polars.from_arrow(table)
            print(pt.sort("_commit_version", descending=True))
        except Exception as e:
            print(f'Error reading changes for {DELTA_TABLE_URI} due to {e}')
            raise e

if __name__ == '__main__':
    job = ReadChangesJob.run()

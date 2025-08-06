from deforestation_copernicus.io.sentinel_hub.nvdi import NvdiFetcher
from deforestation_copernicus.core.utils.config import CoppernicusConfig
from deforestation_copernicus.io.geoalchemy_client import GeoAlchemyClient
from deforestation_copernicus.io.data_models import SentinelHubResult
from typing import Iterable
from datetime import datetime

class Job():
    def __init__(self):
        self.config = CoppernicusConfig()
        self.fetcher = NvdiFetcher(config=self.config)
        self.db_client = GeoAlchemyClient()

    def run(self,
            coordinates_wgs84: tuple,
            resolution: int,
            timestamp_start: datetime,
            timestamp_end: datetime,
            ):
        # TODO this needs to be finished.
        '''
        queries SQL for polygon within given coordinates. if it's not available it queries SentinulHub.
        if it's available it just returns the image from the given path and crops it to respect the input coordinates
        '''
        results: Iterable[SentinelHubResult] = self.fetcher.run(coordinates_wgs84=coordinates_wgs84,
                                                                resolution=resolution,
                                                                timestamp_start=timestamp_start,
                                                                timestamp_end=timestamp_end,
                                                                )
        self.db_client.add_data(results)



if __name__ == '__main__':
    coordinates_wgs84 = (46.16, -16.15, 46.51, -15.58)
    resolution = 60
    timestamp_start=datetime(year=2020,month=6, day=12)
    timestamp_end=datetime(year=2020,month=6, day=30)
    job = Job()
    job.run(coordinates_wgs84=coordinates_wgs84,
            resolution=resolution,
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end)
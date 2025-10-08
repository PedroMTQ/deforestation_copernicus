from datetime import datetime, timezone
from typing import Iterable

from deforestation_copernicus.core.image_merger import ImageMerger
from deforestation_copernicus.core.utils.config import CoppernicusConfig
from deforestation_copernicus.core.utils.utils import get_polygon
from deforestation_copernicus.core.data_models.sentinel_hub_result import SentinelHubResult
from deforestation_copernicus.io.geoalchemy_client import GeoAlchemyClient
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.io.sentinel_hub.nvdi import NvdiFetcher


class Job():
    MINIMUM_OVERLAP = 0.7
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
        '''
        1. queries DB for all polygons within given coordinates. if it's not available it queries SentinulHub.
        performs DB query

        '''
        polygon = get_polygon(coordinates_wgs84=coordinates_wgs84)
        results: Iterable[SentinelHubResult] = self.db_client.get(polygon=polygon,
                                                                  resolution=resolution,
                                                                  timestamp_start=timestamp_start,
                                                                  timestamp_end=timestamp_end,
                                                                  )
        polygon_overlap = ImageMerger(results).check_overlap(minimum_overlap=self.MINIMUM_OVERLAP)
        return
        if not polygon_overlap:
            results: Iterable[SentinelHubResult] = self.fetcher.run(coordinates_wgs84=coordinates_wgs84,
                                                                    resolution=resolution,
                                                                    timestamp_start=timestamp_start,
                                                                    timestamp_end=timestamp_end,
                                                                    )
            self.db_client.add_data(results)
        results: Iterable[SentinelHubResult] = self.db_client.get(polygon=polygon,
                                                                  resolution=resolution,
                                                                  timestamp_start=timestamp_start,
                                                                  timestamp_end=timestamp_end,
                                                                  )
        logger.debug(f'Trying to get interesecting polygons for {polygon} and found {results} polygons')
        return results



def test():
    '''fetches data for larger area and then tries get intersection for target area'''
    coordinates_target = (46.21, -15.99, 46.39, -15.72)
    coordinates_map = (46.16, -16.15, 46.51, -15.58)
    resolution = 60
    timestamp_start=datetime(year=2020,month=6, day=12, tzinfo=timezone.utc)
    timestamp_end=datetime(year=2020,month=6, day=30, tzinfo=timezone.utc)
    job = Job()
    # data = job.fetcher.run(coordinates_wgs84=coordinates_map,
    #                        resolution=resolution,
    #                        timestamp_start=timestamp_start,
    #                        timestamp_end=timestamp_end)
    # job.db_client.add_data(data)
    results = job.run(coordinates_wgs84=coordinates_target,
                      resolution=resolution,
                      timestamp_start=timestamp_start,
                      timestamp_end=timestamp_end)
    print(results)


if __name__ == '__main__':


    # img = Image.open('/home/pedroq/workspace/deforestation_copernicus/data/nvdi/ed7b7c8acd8228ae3154444b59a44096/response.png').convert('RGBA')
    # img2 = img.copy()
    # print(img.size)
    # draw = ImageDraw.Draw(img2)
    # coordinates_target = ((1, 500), (5, 300), (10, 600), (50,350))
    # draw.polygon(coordinates_target, outline="red")
    # # img3 = Image.blend(img, img2, 0.5)
    # img2.save(os.path.join(DATA,'map.png'))


    # coordinates_target = (46.21, -15.99, 46.39, -15.72)
    # coordinates_map = (46.16, -16.15, 46.51, -15.58)
    # polygon_target = get_polygon(coordinates_target)
    # polygon_maps = get_polygon(coordinates_map)
    # multi_polygon = MultiPolygon([polygon_target, polygon_maps])
    # fig, ax = plt.subplots()
    # for poly in multi_polygon.geoms:
    #     xe, ye = poly.exterior.xy
    #     ax.plot(xe, ye, color="blue")
    # plt.savefig(os.path.join(DATA,'plot.png'))
    test()

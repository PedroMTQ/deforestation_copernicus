import os
from datetime import datetime
from pathlib import Path
from typing import Iterable

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import from_shape
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    MimeType,
    SentinelHubRequest,
    bbox_to_dimensions,
)

from deforestation_copernicus.core.utils.config import CoppernicusConfig
from deforestation_copernicus.core.utils.evalscripts import NVDI
from deforestation_copernicus.core.utils.utils import get_polygon
from deforestation_copernicus.io.data_models import SentinelHubResult
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.settings import DATA


class NvdiFetcher():
    IMAGE_TYPE = 'nvdi'
    DATA_FOLDER = os.path.join(DATA, 'nvdi')
    def __init__(self, config: CoppernicusConfig):
        self.config = config

    def __get_from_api(self,
                       time_interval: tuple[str, str],
                       aoi_bbox: BBox,
                       aoi_size: tuple[int,int]) -> SentinelHubRequest:
        return SentinelHubRequest(evalscript=NVDI,
                                  data_folder=self.DATA_FOLDER,
                                  input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A.define_from(name="s2l2a",
                                                                                                                                     service_url="https://sh.dataspace.copernicus.eu"),
                                  time_interval=time_interval,
                                  other_args={"dataFilter": {"mosaickingOrder": "leastCC"}},
                                  )
                                  ],
                                  responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
                                  bbox=aoi_bbox,
                                  size=aoi_size,
                                  config=self.config.config,
                              )
    def run(self,
            coordinates_wgs84: tuple,
            resolution: int,
            timestamp_start: datetime,
            timestamp_end: datetime,
            ) -> Iterable[SentinelHubResult]:
        '''
        gets image path from db if it exists, otherwise queries copernicus and stores all in DB
        '''
        logger.debug(f'Fetching {self.IMAGE_TYPE} data for coordinates {coordinates_wgs84} from {timestamp_start} to {timestamp_end} (resolution: {resolution})')
        aoi_bbox = BBox(bbox=coordinates_wgs84, crs=CRS.WGS84)
        aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)
        sentinel_hub_request = self.__get_from_api(time_interval=(timestamp_start, timestamp_end), aoi_bbox=aoi_bbox, aoi_size=aoi_size)
        file_name_list = sentinel_hub_request.get_filename_list()
        polygon = get_polygon(coordinates_wgs84=coordinates_wgs84)
        geometry: WKBElement = from_shape(polygon, srid=4326)
        # ! get_data saves the data to disk
        for data_idx, _ in enumerate(sentinel_hub_request.get_data(save_data=True)):
            file_name = file_name_list[data_idx]
            srid = str(Path(file_name).parent)
            image_type = self.IMAGE_TYPE
            image_path = os.path.join(self.DATA_FOLDER, file_name)
            yield SentinelHubResult(srid=srid,
                                    resolution=resolution,
                                    timestamp_start=timestamp_start,
                                    timestamp_end=timestamp_end,
                                    geometry=geometry,
                                    image_type=image_type,
                                    image_path=image_path,
                                    )


if __name__ == '__main__':
    fetcher = NvdiFetcher(config=CoppernicusConfig())
    coordinates_wgs84 = (46.16, -16.15, 46.51, -15.58)
    resolution = 60
    results = fetcher.run(coordinates_wgs84=coordinates_wgs84,
                          resolution=resolution,
                          timestamp_start=datetime(year=2020,month=6, day=12),
                          timestamp_end=datetime(year=2020,month=6, day=30),
                          )
    for i in results:
        print(i.image_path)

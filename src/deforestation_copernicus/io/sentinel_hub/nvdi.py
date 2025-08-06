from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubCatalog,
    SentinelHubRequest,
    SentinelHubStatistical,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType,
    Geometry,
)
from pathlib import Path

from deforestation_copernicus.core.utils.evalscripts import NVDI
from deforestation_copernicus.core.utils.config import CoppernicusConfig
from deforestation_copernicus.settings import DATA
import cv2
import os
from deforestation_copernicus.io.data_models import SentinelHubResult
from geoalchemy2.shape import from_shape
from datetime import datetime
from shapely.geometry import Polygon
from typing import Iterable

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
        aoi_bbox = BBox(bbox=coordinates_wgs84, crs=CRS.WGS84)
        aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)
        sentinel_hub_request = self.__get_from_api(time_interval=(timestamp_start, timestamp_end), aoi_bbox=aoi_bbox, aoi_size=aoi_size)
        file_name_list = sentinel_hub_request.get_filename_list()
        data_list = sentinel_hub_request.get_data(save_data=True)
        x_min, y_min, x_max, y_max = aoi_bbox
        shapely_polygon = Polygon([
                                    (x_min, y_min),
                                    (x_max, y_min),
                                    (x_max, y_max),
                                    (x_min, y_max),
                                    (x_min, y_min)
                                ])
        for data_idx, _ in enumerate(data_list):
            file_name = file_name_list[data_idx]
            srid = str(Path(file_name).parent)
            geometry =  from_shape(shapely_polygon, srid=4326)
            image_type = self.IMAGE_TYPE
            image_path = os.path.join(self.DATA_FOLDER, file_name)
            print(srid, geometry, image_type, image_path)
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
  
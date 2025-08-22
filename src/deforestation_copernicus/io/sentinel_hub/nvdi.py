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
from deforestation_copernicus.core.data_models.sentinel_hub_result import SentinelHubResult
from deforestation_copernicus.io.logger import logger
from deforestation_copernicus.settings import DATA


class NvdiFetcher():
    IMAGE_TYPE = 'nvdi'
    @staticmethod
    def _get_from_api(data_folder: str,
                      time_interval: tuple[str, str],
                      aoi_bbox: BBox,
                      aoi_size: tuple[int,int],
                      config: CoppernicusConfig) -> SentinelHubRequest:
        return SentinelHubRequest(evalscript=NVDI,
                                  data_folder=data_folder,
                                  input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A.define_from(name="s2l2a",
                                                                                                                                     service_url="https://sh.dataspace.copernicus.eu"),
                                  time_interval=time_interval,
                                  other_args={"dataFilter": {"mosaickingOrder": "leastCC"}},
                                  )
                                  ],
                                  responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
                                  bbox=aoi_bbox,
                                  size=aoi_size,
                                  config=config.config,
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

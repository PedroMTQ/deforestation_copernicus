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
from deforestation_copernicus.io.sentinel_hub.nvdi import NvdiFetcher
from deforestation_copernicus.io.sentinel_hub.true_color import TrueColorFetcher
from deforestation_copernicus.core.utils.config import CoppernicusConfig
from deforestation_copernicus.core.utils.utils import get_polygon
from deforestation_copernicus.core.data_models.satellite_data import SatelliteData
from deforestation_copernicus.core.data_models.sentinel_hub_result import SentinelHubResult
from deforestation_copernicus.io.logger import logger
import tempfile


class SentinelHubFetcher():
    def __init__(self, config: CoppernicusConfig, data_folder: str):
        self.config = config
        self.data_folder = data_folder


    def _get_from_api(self, satellite_data: SatelliteData):
        if satellite_data.image_type == 'nvdi':
            return NvdiFetcher._get_from_api(data_folder=self.data_folder,
                                             time_interval=(satellite_data.timestamp_start,
                                                            satellite_data.timestamp_end),
                                             aoi_bbox=satellite_data.bounding_box,
                                             aoi_size=satellite_data.dimensions,
                                             config=self.config)
        elif satellite_data.image_type == 'true_color':
            return TrueColorFetcher._get_from_api(data_folder=self.data_folder,
                                                  time_interval=(satellite_data.timestamp_start,
                                                                 satellite_data.timestamp_end),
                                                  aoi_bbox=satellite_data.bounding_box,
                                                  aoi_size=satellite_data.dimensions,
                                                  config=self.config)

    def run(self, satellite_data: SatelliteData) -> Iterable[SentinelHubResult]:
        '''
        gets image path from db if it exists, otherwise queries copernicus and stores all in DB
        '''
        logger.debug(f'Fetching data for {satellite_data})')
        sentinel_hub_request = self._get_from_api(satellite_data)
        file_name_list = sentinel_hub_request.get_filename_list()
        minio_path = satellite_data.get_minio_path()
        polygon = get_polygon(bbox=satellite_data.bounding_box)
        geometry: WKBElement = from_shape(polygon, srid=4326)
        # ! get_data saves the data to disk
        for data_idx, _ in enumerate(sentinel_hub_request.get_data(save_data=True)):
            # TODO should image_path have file_name or srid?
            file_name = file_name_list[data_idx]
            srid = str(Path(file_name).parent)
            image_type = satellite_data.image_type
            image_path = os.path.join(minio_path, file_name)
            yield SentinelHubResult(srid=srid,
                                    resolution=satellite_data.resolution,
                                    timestamp_start=satellite_data.timestamp_start,
                                    timestamp_end=satellite_data.timestamp_end,
                                    geometry=geometry,
                                    image_type=image_type,
                                    image_path=image_path,
                                    )

from dataclasses import asdict, dataclass, field, fields
from datetime import datetime
from sentinelhub import (
    CRS,
    BBox,
    bbox_to_dimensions)
from typing import Literal
from deforestation_copernicus.settings import PARTITION_GEOHASH_LEVEL
import pygeohash

DATE_FORMAT = '%Y-%m-%d'
AVAILABLE_IMAGE_TYPES = Literal['nvdi', 'true_color']

@dataclass
class SatelliteData():
    min_longitude: float
    max_longitude: float
    min_latitude: float
    max_latitude: float
    resolution: int
    timestamp_start: datetime
    timestamp_end: datetime
    image_type: AVAILABLE_IMAGE_TYPES
    bounding_box: BBox = field(default=None, repr=False)
    dimensions: tuple = field(default=None)
    tiff_path: str = field(default=None)
    cog_image: str = field(default=None)
    geohash: str = field(default=None)

    def get_center(self) -> dict:
        center_longitude = (self.min_longitude + self.max_longitude) / 2
        center_latitude = (self.min_latitude + self.max_latitude) / 2
        return {
            'longitude': center_longitude,
            'latitude': center_latitude
            }

    def __post_init__(self):
        self.bounding_box = BBox(bbox={'min_x': self.min_longitude,
                                       'max_x': self.max_longitude,
                                       'min_y': self.min_latitude,
                                       'max_y': self.max_latitude}, crs=CRS.WGS84)
        self.dimensions = bbox_to_dimensions(self.bounding_box, resolution=self.resolution)
        if not self.geohash:
            bounding_box_center = self.get_center()
            self.geohash = pygeohash.encode(latitude=bounding_box_center['latitude'],
                                            longitude=bounding_box_center['longitude'],
                                            precision=PARTITION_GEOHASH_LEVEL)



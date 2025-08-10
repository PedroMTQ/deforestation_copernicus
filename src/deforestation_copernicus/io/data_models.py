
from dataclasses import dataclass, field, fields
from datetime import datetime

import rasterio
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from sentinelhub import (
    CRS,
    BBox,
    bbox_to_dimensions,
)
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import registry

mapper_registry = registry()

class BaseDataclass():
    pass

@mapper_registry.mapped
@dataclass
class SentinelHubResult(BaseDataclass):
    __tablename__ = 'sentinel_hub_result'
    __sa_dataclass_metadata_key__ = "sa"

    srid: str = field(metadata={"sa": Column(String, primary_key=True)}, repr=False)
    resolution: int = field(metadata={"sa": Column(Integer)})
    timestamp_start: datetime = field(metadata={"sa": Column(DateTime)})
    timestamp_end: datetime = field(metadata={"sa": Column(DateTime)})
    # srid 4326 since we use WGS84 for querying sentinelhub
    geometry: WKBElement = field(metadata={"sa": Column(Geometry('POLYGON', srid=4326), index=True)})
    image_type: str = field(metadata={"sa": Column(String)})
    image_path: str = field(metadata={"sa": Column(String)})

    def __repr__(self):
        res = []
        for f in fields(self):
            if not f.repr:
                continue
            value = getattr(self, f.name)
            if f.name == 'geometry':
                value = self.polygon
            res.append(f'{f.name}={value}')
        res = ', '.join(res)
        return f'{self.__class__.__name__}({res})'

    @property
    def polygon(self):
        if not hasattr(self, '_polygon'):
            self._polygon = to_shape(self.geometry)
        return self._polygon

    @property
    def bounding_box(self):
        if not hasattr(self, '_bounding_box'):
            self._bounding_box = BBox(bbox=self.polygon.bounds, crs=CRS.WGS84)
        return self._bounding_box

    @property
    def bounding_box_size(self):
        if not hasattr(self, '_bounding_box_size'):
            self._bounding_box_size = bbox_to_dimensions(self.bounding_box, resolution=self.resolution)
        return self._bounding_box_size

    @property
    def raster(self):
        if not hasattr(self, '_raster'):
            west, south, east, north = self.bounding_box
            width, height = self.bounding_box_size
            self._raster = rasterio.transform.from_bounds(west=west, south=south, east=east, north=north, width=width,height=height)
        return self._raster



if __name__ == '__main__':
    print(SentinelHubResult)

from sentinelhub import (
    CRS,
    BBox,
)
from shapely.geometry import Polygon


def get_polygon(coordinates_wgs84: tuple) -> Polygon:
    aoi_bbox = BBox(bbox=coordinates_wgs84, crs=CRS.WGS84)
    x_min, y_min, x_max, y_max = aoi_bbox
    return Polygon([
                    (x_min, y_min),
                    (x_max, y_min),
                    (x_max, y_max),
                    (x_min, y_max),
                    (x_min, y_min)
                ])

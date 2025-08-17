from sentinelhub import (
    CRS,
    BBox,
)
from shapely.geometry import Polygon
import json
from datetime import datetime, timedelta, timezone
from typing import Iterable

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





def batch_yielder(initial_yielder: Iterable[dict], batch_size: int) -> Iterable[list[dict]]:
    batch = []
    for item in initial_yielder:
        if len(batch) >= batch_size:
            yield batch
            batch = []
        batch.append(item)
    if batch:
        yield batch

def get_current_time():
    return datetime.now(timezone.utc)

def deserializer(x):
    if x:
        return json.loads(x.decode('utf-8'))
    return x

def serializer(x):
    if x:
        return json.dumps(x, cls=DateTimeEncoder).encode('utf-8')
    return x


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return obj.total_seconds()
        else:
            return super().default(obj)

def get_table_delta_uri(delta_bucket: str, delta_table: str) -> str:
    return f's3a://{delta_bucket}/{delta_table}'

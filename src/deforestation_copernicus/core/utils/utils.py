from sentinelhub import (
    CRS,
    BBox,
)
from shapely.geometry import Polygon
import json
from datetime import datetime, timedelta, timezone
from typing import Iterable
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

COG_PROFILE = cog_profiles.get("deflate")
COG_PROFILE.update({"crs": "EPSG:4326"})

def get_polygon(min_longitude: float=None,
                max_longitude: float=None,
                min_latitude: float=None,
                max_latitude: float=None,
                bbox: BBox=None) -> Polygon:
    if not bbox:
        bbox = BBox(bbox={'min_x': min_longitude,
                          'max_x': max_longitude,
                          'min_y': min_latitude,
                          'max_y': max_latitude},
                              crs=CRS.WGS84)
    x_min, y_min, x_max, y_max = bbox
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


def create_cog(input_path: str,
               output_path: str,
               additional_cog_metadata: dict={},
               add_mask: bool=True,
               ):
    cog_translate(
        source=input_path,
        dst_path=output_path,
        dst_kwargs = COG_PROFILE,
        add_mask=add_mask,
        additional_cog_metadata=additional_cog_metadata,
    )
from dataclasses import asdict, dataclass, field
from datetime import datetime
from sentinelhub import (
    CRS,
    BBox,
    bbox_to_dimensions)
from typing import Literal

DATE_FORMAT = '%Y-%m-%d'
AVAILABLE_IMAGE_TYPES = Literal['nvdi', 'true_color']

@dataclass
class DownloadRequestBoundingBoxWGS84():
    min_longitude: float
    max_longitude: float
    min_latitude: float
    max_latitude: float
    resolution: int
    timestamp_start: datetime
    timestamp_end: datetime
    image_type: AVAILABLE_IMAGE_TYPES


    def to_dict(self) -> dict:
        return asdict(self)


if __name__ == '__main__':
    request_fields = DownloadRequestBoundingBoxWGS84.fields()
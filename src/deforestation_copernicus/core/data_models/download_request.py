from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Literal
from deforestation_copernicus.core.data_models.base import BaseDataModel

DATE_FORMAT = '%Y-%m-%d'
AVAILABLE_IMAGE_TYPES = Literal['nvdi', 'true_color']

@dataclass
class DownloadRequest(BaseDataModel):
    min_longitude: float
    max_longitude: float
    min_latitude: float
    max_latitude: float
    resolution: int
    timestamp_start: datetime
    timestamp_end: datetime
    image_type: AVAILABLE_IMAGE_TYPES




if __name__ == '__main__':
    request_fields = DownloadRequest.fields()
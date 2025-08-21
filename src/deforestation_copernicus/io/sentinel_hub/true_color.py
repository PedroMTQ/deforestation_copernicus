from sentinelhub import (
    BBox,
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
)

from deforestation_copernicus.core.utils.config import CoppernicusConfig
from deforestation_copernicus.core.utils.evalscripts import TRUE_COLOR


class TrueColorFetcher():
    IMAGE_TYPE = 'true_color'

    @staticmethod
    def _get_from_api(data_folder: str,
                      time_interval: tuple[str, str],
                      aoi_bbox: BBox,
                      aoi_size: tuple[int,int],
                      config: CoppernicusConfig) -> SentinelHubRequest:
        return SentinelHubRequest(evalscript=TRUE_COLOR,
                                  data_folder=data_folder,
                                  input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L1C.define_from(name="s2l2a",
                                                                                                                                     service_url="https://sh.dataspace.copernicus.eu"),
                                                                            time_interval=time_interval,
                                                                            # least cloud coverage
                                                                            mosaicking_order=MosaickingOrder.LEAST_CC,
                                                                            other_args={"dataFilter": {"mosaickingOrder": "leastCC"}},
                                                                            )
                                  ],
                                  responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
                                  bbox=aoi_bbox,
                                  size=aoi_size,
                                  config=config.config,
                              ).get_data()




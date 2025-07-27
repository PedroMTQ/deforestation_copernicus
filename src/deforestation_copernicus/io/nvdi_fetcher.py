from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubCatalog,
    SentinelHubRequest,
    SentinelHubStatistical,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType,
    Geometry,
)


from deforestation_copernicus.core.utils.evalscripts import NVDI
from deforestation_copernicus.core.utils.config import CoppernicusConfig
import cv2


class NvdiFetcher():
    def __init__(self, config: CoppernicusConfig):
        self.config = config

    def __get_from_api(self,
                       time_interval: tuple[str, str],
                       aoi_bbox: BBox,
                       aoi_size: tuple[int,int]):
        return SentinelHubRequest(evalscript=NVDI,
                                  input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A.define_from(name="s2l2a",
                                                                                                                                     service_url="https://sh.dataspace.copernicus.eu"),
                                  time_interval=time_interval,
                                  other_args={"dataFilter": {"mosaickingOrder": "leastCC"}},
                                  )
                                  ],
                                  responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
                                  bbox=aoi_bbox,
                                  size=aoi_size,
                                  config=self.config.config,
                              ).get_data()
    def run(self,
            time_interval: tuple[str, str],
            aoi_bbox: BBox,
            aoi_size: tuple[int,int]):
        '''
        gets image path from db if it exists, otherwise queries copernicus and stores all in DB
        '''
        api_results = self.__get_from_api(time_interval=time_interval, aoi_bbox=aoi_bbox, aoi_size=aoi_size)
        return api_results

if __name__ == '__main__':
    import numpy as np
    import cv2
    from PIL import Image



    fetcher = NvdiFetcher(config=CoppernicusConfig())
    aoi_coords_wgs84 = [15.461282, 46.757161, 15.574922, 46.851514]
    resolution = 10
    aoi_bbox = BBox(bbox=aoi_coords_wgs84, crs=CRS.WGS84)
    aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)
    results = fetcher.run(time_interval= ('2025-01-12', '2025-01-14'),
                                          aoi_bbox=aoi_bbox,
                                          aoi_size=aoi_size)
    print(results)
    for idx, np_array in enumerate(results):
        cv2.imwrite(f"data/images/{idx}_cv.png", cv2.cvtColor(np_array, cv2.COLOR_RGB2BGR))
        img = Image.fromarray(np_array)
        img.save(f"data/images/{idx}_pillow.png")
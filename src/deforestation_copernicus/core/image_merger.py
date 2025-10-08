from sentinelhub import CRS

from deforestation_copernicus.core.data_models.sentinel_hub_result import SentinelHubResult


class ImageMerger():
    '''
    uses rasterio to merge SentinelHubResult
    '''
    def __init__(self, images: list[SentinelHubResult]):
        self.images = images

    # TODO continue here
    def check_overlap(self, minimum_overlap):
        '''checks overlap of images'''
        print('HERE',self.images[0].bounding_box, self.images[0].bounding_box_size)
        for image in self.images:
            print(image.raster)
        print(self.images)

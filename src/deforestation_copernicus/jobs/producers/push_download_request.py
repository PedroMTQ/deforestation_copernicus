from deforestation_copernicus.core.messages.download_request import DownloadRequestBoundingBoxWGS84
from deforestation_copernicus.core.download_request_pusher import DownloadRequestPusher
from deforestation_copernicus.io.logger import logger
from datetime import datetime

class PushDownloadRequestJob():
    '''
    Populates mongo DB according to n_customers
    Note that the customer IDs are static since we are using a range and not an UUID
    This is intentional so that we can easily modify and read specific customers within a given range
    '''
    @staticmethod
    def run(requests: list[DownloadRequestBoundingBoxWGS84]):
        DownloadRequestPusher().run(requests)
        logger.info(f'Submitted {requests} to Kafka')

if __name__ == '__main__':
    requests = [DownloadRequestBoundingBoxWGS84(min_longitude=46.16, 
                                                max_longitude=46.51,
                                                min_latitude=-16.15,
                                                max_latitude=-15.58,
                                                resolution=60,
                                                timestamp_start=datetime(year=2020, month=6, day=12),
                                                timestamp_end=datetime(year=2020, month=6, day=20),
                                                image_type='true_color',
                                                )]
    job = PushDownloadRequestJob.run(requests=requests)

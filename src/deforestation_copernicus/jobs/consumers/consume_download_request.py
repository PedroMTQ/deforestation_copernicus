from deforestation_copernicus.core.satellite_data_download.download_request_consumer import DownloadRequestConsumer


class KafkaToDeltaJob():
    def start_service(self):
        consumer = DownloadRequestConsumer()
        while True:
            consumer.run()

if __name__ == '__main__':
    test = KafkaToDeltaJob()
    test.start_service()

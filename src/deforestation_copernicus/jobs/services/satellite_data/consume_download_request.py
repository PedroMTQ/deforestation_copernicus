from deforestation_copernicus.core.services.satellite_data.download_request_consumer import DownloadRequestConsumer


class Job():
    def start_service(self):
        consumer = DownloadRequestConsumer()
        while True:
            consumer.run()

if __name__ == '__main__':
    test = Job()
    test.start_service()

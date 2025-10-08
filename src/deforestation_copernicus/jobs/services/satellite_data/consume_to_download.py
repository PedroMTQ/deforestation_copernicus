from deforestation_copernicus.core.services.satellite_data.to_download_consumer import ToDownloadConsumer


class Job():
    def start_service(self):
        consumer = ToDownloadConsumer()
        while True:
            consumer.run()

if __name__ == '__main__':
    test = Job()
    test.start_service()

from kafka_deltalake_minio.core.kafka_to_delta_consumer import KafkaToDeltaConsumer


class KafkaToDeltaJob():
    def start_service(self):
        consumer = KafkaToDeltaConsumer()
        while True:
            consumer.run()

if __name__ == '__main__':
    test = KafkaToDeltaJob()
    test.start_service()

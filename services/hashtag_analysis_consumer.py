from kafka import KafkaConsumer
import json
import multiprocessing


class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        print('started')
        consumer = KafkaConsumer(bootstrap_servers='127.0.0.1:9092',
                                 consumer_timeout_ms=5000,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 auto_offset_reset='earliest',
                                 group_id=None,
                                 client_id="reader",
                                 api_version=(0, 10))
        consumer.subscribe(['TrendingHashtagAnalysis'])

        #TODO: For some reason no messages are read! This could be due to wrong cluster config, but other app can read successfully. Hm?!
        while not self.stop_event.is_set():
            print(consumer.poll())
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

        consumer.close()

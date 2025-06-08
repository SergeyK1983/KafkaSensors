import json
import logging
import socket

from django.conf import settings
from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import ClusterMetadata


logger = logging.getLogger(__name__)


class ObjectHeatPointProducer:

    TOPIC: str = "object_heat_point"
    CONF: dict = {
        "bootstrap.servers": settings.KAFKA_CONFIG["bootstrap_servers"],
        "client.id": socket.gethostname(),
        # Fixed properties
        "acks": "all"  # Alias for request.required.acks, int -1..1000, -1='all'
    }
    producer = Producer(CONF)

    def __init__(self):
        ObjectHeatPointProducer.check_topic()

    @classmethod
    def check_topic(cls):
        cluster_metadata: ClusterMetadata = cls.producer.list_topics(timeout=100)
        if cls.TOPIC not in cluster_metadata.topics:
            err = KafkaError(KafkaError.UNKNOWN_TOPIC_OR_PART)
            raise KafkaException(err)

    @staticmethod
    def delivery_callback(err, msg):
        if err:
            logger.error('ERROR: Message failed delivery: {}'.format(err))
        else:
            logger.info("Produced event to topic {topic}: key = {key:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8')
            ))

    def send(self, msg: str | dict | None = None):

        if msg is None:
            value = "нет сообщений"
        elif not isinstance(msg, (str, dict)):
            raise TypeError("msg must be str or dict")
        elif isinstance(msg, str):
            value = msg
        else:
            value = json.dumps(msg)

        # try:
        #     self.producer.init_transactions(1.0)
        # except KafkaException as exc:
        #     error: KafkaError = exc.args[0]
        #     logger.error("Ошибка1: %s, %s, %s" % (error.str(), error.code(), error.name()))

        # try:
        #     self.producer.begin_transaction()
        # except KafkaException as exc:
        #     error: KafkaError = exc.args[0]
        #     logger.error("Ошибка2: %s, %s, %s" % (error.str(), error.code(), error.name()))
        #     # self.producer.abort_transaction()

        try:
            self.producer.produce(topic=self.TOPIC, value=value, key="heat_point", callback=self.delivery_callback)  # асинхронная функция
        except KafkaException as exc:
            error: KafkaError = exc.args[0]
            logger.error("Ошибка3: %s, %s, %s" % (error.str(), error.code(), error.name()))
            # self.producer.abort_transaction()

        # try:
        #     self.producer.commit_transaction(1.0)
        # except KafkaException as exc:
        #     error: KafkaError = exc.args[0]
        #     logger.error("Ошибка4: %s, %s, %s" % (error.str(), error.code(), error.name()))
        #     self.producer.abort_transaction()
        # print(f"Topics: {cluster_metadata.__dict__}")

        self.producer.poll(10)
        self.producer.flush()

        return


object_heat_point_producer = ObjectHeatPointProducer()


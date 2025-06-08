
from django.conf import settings
from confluent_kafka import Consumer


class ObjectHeatPointConsumer:
    """ Потребитель для объекта: ИТП "Центральный" """

    TOPIC: str = "object_heat_point"
    CONF = {
        "bootstrap.servers": settings.KAFKA_CONFIG["bootstrap_servers"],
        "group.id": "heat_point_center",
        "auto.offset.reset": "earliest"
    }

    def create_consumer(self) -> Consumer:
        """
        Создает потребителя для прослушивания топика object_heat_point (объект: ИТП "Центральный")
        :return: instance Consumer
        """
        consumer = Consumer(self.CONF)
        consumer.subscribe([self.TOPIC])
        return consumer


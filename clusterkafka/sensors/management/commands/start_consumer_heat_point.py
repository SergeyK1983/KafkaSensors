import logging

from django.core.management.base import BaseCommand
from confluent_kafka.cimpl import Consumer, Message

from sensors.kafka.consumers import ObjectHeatPointConsumer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запуск потребителя для топика 'object_heat_point'"

    def handle(self, *args, **options):
        consumer: Consumer = ObjectHeatPointConsumer().create_consumer()

        try:
            while True:
                msg: Message = consumer.poll(1.0)
                if msg is None:
                    # Initial message consumption may take up to
                    # `session.timeout.ms` for the consumer group to
                    # rebalance and start consuming
                    print("Waiting...")
                elif msg.error():
                    print("ERROR: %s".format(msg.error()))
                else:
                    # Extract the (optional) key and value, and print.
                    # print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    #     topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                    print(f"{msg.key()}: {msg.value()}")
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            consumer.close()

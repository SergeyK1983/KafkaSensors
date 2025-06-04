import logging

from django.core.management.base import BaseCommand, CommandError
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic, KafkaError, KafkaException

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Создание топика для кластера Кафка"

    def add_arguments(self, parser):
        parser.add_argument("-tm", "--topic_name", type=str, help="Наименование топика Кафка")

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Будут создана тема (топик) для Kafka")
        )
        if not options["topic_name"]:
            raise CommandError("Error: Должно быть указано наименование создаваемого топика")

        name: str = options["topic_name"]

        topic = NewTopic(
            topic=name,
            num_partitions=1,
            replication_factor=3,
        )

        conf: dict = {
            "bootstrap.servers": "localhost:30940,localhost:30941,localhost:30942",
            "socket.timeout.ms": 2000
        }
        try:
            admin = AdminClient(conf=conf)
            result: dict = admin.create_topics(new_topics=[topic])
            for name_topic, future in result.items():
                future.result()

            self.stdout.write(
                self.style.NOTICE(f"Топики: {result}")
            )
            logger.info(f"Создан топик {name}")
        except KafkaException as e:
            error: KafkaError = e.args[0]
            self.stderr.write(
                self.style.ERROR("Ошибка: %s, %s, %s" % (error.str(), error.code(), error.name()))
            )
            logger.error("Ошибка: %s, %s, %s" % (error.str(), error.code(), error.name()))
            # INVALID_REPLICATION_FACTOR
        except CommandError as e:
            self.stderr.write(self.style.ERROR(f"Команда провалилась: {str(e)}"))
            logger.error(f"Команда провалилась: {str(e)}")
        else:
            self.stdout.write(self.style.SUCCESS("Тема (топик) для Kafka создана"))


import logging

from django.core.management.base import BaseCommand, CommandError
from confluent_kafka.admin import AdminClient, TopicMetadata
from confluent_kafka.cimpl import NewTopic, KafkaError, KafkaException

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Создание топика для кластера Кафка"

    def add_arguments(self, parser):
        parser.add_argument("-tm", "--topic_name", type=str, help="Наименование топика Кафка")

        parser.add_argument("-p", "--partitions", type=int, default=3, help="Количество партиций в топике")

        parser.add_argument(
            "-rf", "--replication_factor", type=int, default=3, help="Количество реплик, в диапазоне 1..3 или -1"
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Создается тема (топик) для Kafka")
        )
        if not options["topic_name"]:
            raise CommandError("Error: Должно быть указано наименование создаваемого топика")

        name: str = options["topic_name"]
        partitions: int = options["partitions"]
        replication_factor: int = options["replication_factor"]

        if replication_factor not in (-1, 1, 2, 3):
            raise CommandError("Error: Количество реплик должно быть в диапазоне 1..3 или -1")

        # ValueError: num_partitions out of expected range 1..100000 or -1 for broker default
        if partitions not in range(1, 51) and partitions != -1:
            raise CommandError("Error: Количество разделов должно быть в диапазоне 1..50 или -1")

        topic = NewTopic(
            topic=name,
            num_partitions=partitions,
            replication_factor=replication_factor,
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

            created_topic: list[str] = list(result.keys())
        except KafkaException as e:
            error: KafkaError = e.args[0]
            self.stderr.write(
                self.style.ERROR("Ошибка: %s, %s, %s" % (error.str(), error.code(), error.name()))
            )
            logger.error("Ошибка: %s, %s, %s" % (error.str(), error.code(), error.name()))
            # INVALID_REPLICATION_FACTOR
        except CommandError as e:
            self.stderr.write(
                self.style.ERROR(f"Команда провалилась: {str(e)}")
            )
            logger.error(f"Команда провалилась: {str(e)}")
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Создана тема (топик): {created_topic}")
            )
            logger.info(f"Создан топик {created_topic}")


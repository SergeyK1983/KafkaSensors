import logging

from django.core.management.base import BaseCommand, CommandError
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import KafkaError, KafkaException

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Удаление топиков из кластера Кафка"

    def add_arguments(self, parser):
        parser.add_argument("topics", nargs="+", type=str, help="Наименования топиков Кафка")

    def handle(self, *args, **options):

        names: list[str] = options["topics"]

        conf: dict = {
            "bootstrap.servers": "localhost:30940,localhost:30941,localhost:30942",
            "socket.timeout.ms": 2000
        }
        try:
            admin = AdminClient(conf=conf)
            result: dict = admin.delete_topics(topics=names)

            for name_topic, future in result.items():
                future.result()

            deleted_topics: list[str] = list(result.keys())

        except KafkaException as e:
            error: KafkaError = e.args[0]
            self.stderr.write(
                self.style.ERROR("Ошибка: %s, %s, %s" % (error.str(), error.code(), error.name()))
            )
            logger.error("Ошибка: %s, %s, %s" % (error.str(), error.code(), error.name()))
        except CommandError as e:
            self.stderr.write(
                self.style.ERROR(f"Команда провалилась: {str(e)}")
            )
            logger.error(f"Команда провалилась: {str(e)}")
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Удалена тема (топик): {deleted_topics}")
            )
            logger.info(f"Удалена тема (топик): {deleted_topics}")


import json
import time
import asyncio
import logging
from datetime import datetime
from aiohttp import ClientSession, ClientTimeout, ClientResponseError, ClientError

from sensors.common import AsIterator
from sensors.constants import PATH_SEND_TELEMETRY
from sensors.exceptions import SensorResponseException
from sensors.fake_connector import FakeConnector
from sensors.serializers.telemetry import TelemetrySerializer


logger = logging.getLogger(__name__)


async def sender(wait_sec: int | float) -> None:
    """ Для проверок """

    print(f"погнали {datetime.now().strftime('%H:%M:%S.%f') = }")
    data: dict = FakeConnector.input_data()
    serializer = TelemetrySerializer(data=data)
    serializer.is_valid(raise_exception=True)

    # Условная обработка принятого сообщения телеметрии:
    await asyncio.sleep(wait_sec)
    print(f"пригнали {datetime.now().strftime('%H:%M:%S.%f') = }")
    return None


async def send_fake_telemetry(count: int):
    """ Отправляем как бы телеметрию раз в секунду """

    timeout = ClientTimeout(total=0.7)
    async with ClientSession(base_url=PATH_SEND_TELEMETRY, timeout=timeout) as session:
        async for i in AsIterator(count):
            start: float = time.perf_counter()  # счетчик производительности, включает время, прошедшее во время сна
            data: dict = FakeConnector.input_data()
            try:
                async with session.post("input-telemetry/", json=data) as response:  # application/json auto
                    status: int = response.status
                    message = await response.json()
                    SensorResponseException.raise_status_exception(response, message)
                    print(f"{status = } -> {datetime.now().strftime('%H:%M:%S.%f')} -> {message}")
            except asyncio.exceptions.TimeoutError:
                logger.error(msg=f"TimeoutError, {datetime.now()}")
            except ClientResponseError as err:
                logger.error(msg=f"ClientResponseError: status = {err.status}, {err.message}")
            except ClientError as err:
                logger.error(msg=f"ClientError: msg = {err}")

            end: float = time.perf_counter()
            delay: float = 1 - (end - start) if end - start < 1 else 0
            print(f"{delay = }")
            await asyncio.sleep(delay)
    return


async def task_with_fake_telemetry(data: dict) -> None:
    """ Тут условно что-то делаем с полученной телеметрией """

    # как бы работаем только в нашем сервисе за примерно одинаковое время,
    # чтобы гарантировать соответствие очередности поступающих данных
    await asyncio.sleep(2)
    print(f"Из задачи по обработке: {datetime.now().strftime('%H:%M:%S.%f')}, {tuple(data.keys())}")
    return

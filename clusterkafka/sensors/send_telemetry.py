import json
import time
import asyncio
from random import randint
from datetime import datetime
from aiohttp import ClientSession

from sensors.common import AsIterator
from sensors.fake_connector import FakeConnector
from sensors.serializers.telemetry import TelemetrySerializer


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

    async with ClientSession("http://localhost:8020/sensors/") as session:
        async for i in AsIterator(count):
            start: float = time.perf_counter()  # счетчик производительности, включает время, прошедшее во время сна
            data: str = json.dumps(FakeConnector.input_data())
            async with session.post("input-telemetry/", json=data) as response:
                status: int = response.status
                print(f"{status = } -> {datetime.now().strftime('%H:%M:%S.%f')} -> {await response.json()}")

            end: float = time.perf_counter()
            delay: float = 1 - (end - start) if end - start < 1 else 0
            print(f"{delay = }")
            await asyncio.sleep(delay)
    return


async def task_with_fake_telemetry(data: dict) -> None:
    """ Тут условно что-то делаем с полученной телеметрией """

    await asyncio.sleep(randint(2, 7))
    print(f"Из задачи {datetime.now().strftime('%H:%M:%S.%f')} {tuple(data.keys())}")
    return

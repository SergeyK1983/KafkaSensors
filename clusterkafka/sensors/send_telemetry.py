import time
import asyncio
from random import randint
from datetime import datetime

from sensors.common import AsIterator
from sensors.fake_connector import FakeConnector
from sensors.serializers.telemetry import TelemetrySerializer


async def sender(wait_sec: int | float) -> None:
    print(f"погнали {datetime.now().strftime('%H:%M:%S.%f') = }")
    data: dict = FakeConnector.input_data()
    serializer = TelemetrySerializer(data=data)
    serializer.is_valid(raise_exception=True)

    # Условная обработка принятого сообщения телеметрии:
    await asyncio.sleep(wait_sec)
    print(f"пригнали {datetime.now().strftime('%H:%M:%S.%f') = }")
    return None


async def amount_sending(count: int) -> None:
    async for i in AsIterator(count):
        # условно сообщения поступают раз в секунду
        start: float = time.perf_counter()  # счетчик производительности, включает время, прошедшее во время сна
        task = asyncio.create_task(sender(wait_sec=randint(2, 7)))  # noqa
        end: float = time.perf_counter()
        delay: float = 1 - (end - start) if end - start < 1 else 0
        print(f"{delay = }")
        await asyncio.sleep(delay)
    return


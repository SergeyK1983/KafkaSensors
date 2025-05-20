import asyncio
import json
import time
import logging
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from sensors.fake_connector import FakeConnector
from sensors.send_telemetry import sender, send_fake_telemetry, task_with_fake_telemetry
from sensors.serializers.telemetry import TelemetrySerializer, ShipmentsSerializer


logger = logging.getLogger(__name__)


class TelemetryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TelemetrySerializer

    def get(self, request, *args, **kwargs):
        """
        API для просмотра примера полученных и подготовленных входных данных объектов телеметрии для последующей
        передачи.
        """

        serializer = self.serializer_class(data=FakeConnector.input_data())
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)


class TelemetrySenderListCreateAPIView(generics.ListCreateAPIView):
    """ Синхронно отправляет некоторое количество сообщений условно раз в секунду. """

    http_method_names = ["post"]
    serializer_class = ShipmentsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        number_shipments: int = serializer.validated_data["number_shipments"]

        for i in range(number_shipments):
            start: datetime = datetime.now()
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S') = }")
            time.sleep(1)
            connector = TelemetrySerializer(data=FakeConnector.input_data())
            connector.is_valid()
            if connector.errors:
                logger.error(connector.errors)
            # Отправляем connector.validated_data в кафка
            # ...
            finish: timedelta = datetime.now() - start
            print(f"{str(finish) = }")

        return Response(f"Успешно, количество отправлений: {number_shipments}", status=status.HTTP_200_OK)


@require_GET
async def three_telemetry(request):
    """ Три задачи """

    # asyncio.TaskGroup() in python 3.11
    start_time = time.time()  # время UTC в [с], * 1000 будут [мс].
    task = asyncio.gather(sender(wait_sec=1), sender(wait_sec=1), sender(wait_sec=1))
    await task
    end_time = time.time()
    print(f"{end_time - start_time = }")
    return JsonResponse(data={"OK": "Передача"}, status=status.HTTP_200_OK)


@csrf_exempt  # только для домашнего использования!
@require_POST
async def sending_fake_telemetry(request):
    """ Отправляет телеметрию раз в секунду. Количество отправлений указано в запросе. """

    data: dict = json.loads(request.body)
    serializer = ShipmentsSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        return JsonResponse(data={"error": exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    number_shipments: int = serializer.validated_data["number_shipments"]
    asyncio.create_task(send_fake_telemetry(count=number_shipments))  # noqa

    return JsonResponse(data={"OK": f"Отправлено сообщений {number_shipments}"}, status=status.HTTP_200_OK)


@csrf_exempt
@require_POST
async def input_telemetry(request):
    """ Принимает входящую телеметрию и обрабатываем """

    # data: dict = json.loads(request.body)
    data: dict = json.loads(json.loads(request.body))
    serializer = TelemetrySerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        return JsonResponse(data={"error": exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    asyncio.create_task(task_with_fake_telemetry(data=serializer.validated_data))  # noqa

    return JsonResponse(data={"OK": f"Прием пришел корректно"}, status=status.HTTP_200_OK)


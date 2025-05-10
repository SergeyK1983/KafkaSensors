import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import AsyncContextManager

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from sensors.fake_connector import FakeConnector
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
            print(f"{start.strftime('%Y-%m-%d %H:%M:%S') = }")
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


async def sender() -> None:
    print("погнали")

    async with AsyncContextManager():
        data: dict = FakeConnector.input_data()

    serializer = TelemetrySerializer(data=data)
    serializer.is_valid(raise_exception=True)
    await asyncio.sleep(1)
    # data = serializer.data
    return None


@csrf_exempt
async def sender_telemetry(request):
    if request.method != "POST":
        return JsonResponse(data={"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    data: dict = json.loads(request.body)
    serializer = ShipmentsSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        return JsonResponse(data={"error": exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    number_shipments: int = serializer.validated_data["number_shipments"]
    await sender()

    return JsonResponse(data={"OK": "Передача"}, status=status.HTTP_200_OK)


import asyncio
import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from sensors.fake_connector import FakeConnector
from sensors.serializers.telemetry import TelemetrySerializer, ShipmentsSerializer


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


async def sender(number_shipments: int) -> None:
    for i in range(0, number_shipments):
        # print("погнали")
        serializer = TelemetrySerializer(data=FakeConnector.input_data())
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
    await sender(number_shipments)

    return JsonResponse(data={"OK": "Передача"}, status=status.HTTP_200_OK)


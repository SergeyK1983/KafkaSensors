from rest_framework import generics, status
from rest_framework.response import Response

from sensors.fake_connector import FakeHeatMeterCenter, FakeHeatPointCenter
from sensors.serializers.telemetry import TelemetrySerializer, HEAT_METER_CENTER, HEAT_POINT_CENTER
from sensors.structures import HeatMeterNamedDC, TelemetryHeatPointNamedDC


class TelemetryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TelemetrySerializer

    def get(self, request, *args, **kwargs):
        """ API для просмотра примера входных данных объектов телеметрии """

        object_heat_meter: HeatMeterNamedDC = FakeHeatMeterCenter.input_data()
        object_heat_point: TelemetryHeatPointNamedDC = FakeHeatPointCenter.input_data()

        data_from_connector: dict = {
            HEAT_METER_CENTER: object_heat_meter.model_dump(),
            HEAT_POINT_CENTER: object_heat_point.model_dump()
        }

        serializer = self.serializer_class(data=data_from_connector)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)


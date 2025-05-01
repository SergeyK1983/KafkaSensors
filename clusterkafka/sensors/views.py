from rest_framework import generics, status
from rest_framework.response import Response

from sensors.fake_connector import FakeConnector
from sensors.serializers.telemetry import TelemetrySerializer


class TelemetryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TelemetrySerializer

    def get(self, request, *args, **kwargs):
        """ API для просмотра примера входных данных объектов телеметрии """

        serializer = self.serializer_class(data=FakeConnector.input_data())
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)


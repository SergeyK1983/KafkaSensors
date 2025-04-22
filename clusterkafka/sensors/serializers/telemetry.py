from typing import Callable
from rest_framework import serializers

from sensors.serializers.telemetry_heat_point import TelemetryHeatPointSerializer, HeatMeterSerializer


class TelemetryHeatMeterNamedSerializer(HeatMeterSerializer):
    name = serializers.CharField(max_length=100, min_length=3, help_text="Наименование по схеме")


class TelemetryHeatPointNamedSerializer(TelemetryHeatPointSerializer):
    name = serializers.CharField(max_length=100, min_length=3, help_text="Наименование по схеме")


OBJECTS_TELEMETRY: dict[str, Callable] = {
    "heat_point": TelemetryHeatPointNamedSerializer,
    "heat_meter": TelemetryHeatMeterNamedSerializer,
}


class TelemetrySerializer(serializers.Serializer):
    """ Телеметрия """
    pass





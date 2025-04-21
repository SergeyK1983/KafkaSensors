from rest_framework import serializers

from sensors.serializers.telemetry_heat_point import TelemetryHeatPointSerializer, HeatMeterSerializer


class HeatMeterNamedSerializer(HeatMeterSerializer):
    name = serializers.CharField(max_length=100, min_length=3, help_text="Наименование по схеме")


class TelemetryHeatPointNamedSerializer(TelemetryHeatPointSerializer):
    name = serializers.CharField(max_length=100, min_length=3, help_text="Наименование по схеме")


OBJECTS_TELEMETRY = {
    "heat_point": TelemetryHeatPointNamedSerializer,
    "heat_meter": HeatMeterNamedSerializer,
}


class TelemetrySerializer(serializers.Serializer):
    """ Телеметрия """
    pass





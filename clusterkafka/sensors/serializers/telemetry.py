from typing import Callable

from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from sensors.constants import RegisteredObjects
from sensors.serializers.telemetry_heat_point import TelemetryHeatPointSerializer, TelemetryHeatMeterSerializer


class TelemetryHeatMeterNamedSerializer(TelemetryHeatMeterSerializer):
    name = serializers.CharField(max_length=100, min_length=3, help_text="Наименование по схеме")


class TelemetryHeatPointNamedSerializer(TelemetryHeatPointSerializer):
    name = serializers.CharField(max_length=100, min_length=3, help_text="Наименование по схеме")


#
# ==== Телеметрия ====
#
OBJECTS_TELEMETRY: dict[str, Callable] = {
    "heat_point": TelemetryHeatPointNamedSerializer,
    "heat_meter": TelemetryHeatMeterNamedSerializer,
}


HEAT_POINT_CENTER: str = RegisteredObjects.HEAT_POINT_CENTER.name.lower()
HEAT_METER_CENTER: str = RegisteredObjects.HEAT_METER_CENTER.name.lower()


fields: dict = {
    HEAT_POINT_CENTER: OBJECTS_TELEMETRY[RegisteredObjects.HEAT_POINT_CENTER.value[1]](
        required=False, allow_null=True, many=False
    ),
    HEAT_METER_CENTER: OBJECTS_TELEMETRY[RegisteredObjects.HEAT_METER_CENTER.value[1]](
        required=False, allow_null=True, many=False
    ),
}


TelemetrySerializer = type("TelemetrySerializer", (serializers.Serializer,), fields)


class ShipmentsSerializer(serializers.Serializer):
    number_shipments = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Количество отправлений с коннекта"
    )

from sensors.constants import RegisteredObjects
from sensors.serializers.telemetry import TelemetrySerializer, HEAT_METER_CENTER, HEAT_POINT_CENTER
from sensors.structures import HeatMeterNamedDC, TelemetryHeatPointNamedDC


class TestTelemetrySerializer:

    def test_validate_data_heat_meter(self, data_for_heat_meter):
        heat_meter_name: str = HEAT_METER_CENTER
        data_heat_meter_center: dict = data_for_heat_meter

        object_heat_meter = HeatMeterNamedDC(
            name=RegisteredObjects.HEAT_METER_CENTER.value[0], **data_heat_meter_center
        )
        data_from_connector: dict = {heat_meter_name: object_heat_meter.model_dump()}
        serializer = TelemetrySerializer(data=data_from_connector)

        assert serializer.is_valid(raise_exception=True) is True

    def test_validate_data_heat_point(self, data_for_heat_point):
        heat_point_name: str = HEAT_POINT_CENTER
        data_heat_point: dict = data_for_heat_point

        object_heat_point = TelemetryHeatPointNamedDC(
            name=RegisteredObjects.HEAT_POINT_CENTER.value[0], **data_heat_point
        )
        data_from_connector: dict = {heat_point_name: object_heat_point.model_dump()}
        serializer = TelemetrySerializer(data=data_from_connector)

        assert serializer.is_valid(raise_exception=True) is True


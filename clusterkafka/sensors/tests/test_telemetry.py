from sensors.constants import RegisteredObjects
from sensors.serializers.telemetry import TelemetrySerializer, HEAT_METER_CENTER, HEAT_POINT_CENTER
from sensors.structures import HeatMeterNamedDC, TelemetryHeatPointNamedDC, ElectricDriveDC, PumpGroupControlModeDC, \
    FrequencyConverterDC


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

        data: dict = serializer.data

        assert data["heat_point_center"]["pump_groups"] is None
        assert data["heat_point_center"]["pumps"] is None

    def test_validate_data_hp_with_pumps(self, data_for_heat_point, data_for_driver):
        """
        Тест телеметрии теплового пункта с полными данными.
        :param data_for_heat_point: Fixture
        :param data_for_driver: Fixture
        """
        heat_point_name: str = HEAT_POINT_CENTER
        data_heat_point: dict = data_for_heat_point

        circ_pump_1 = ElectricDriveDC(**data_for_driver)
        circ_pump_1.is_frequency_converter = True
        circ_pump_1.frequency_converter = FrequencyConverterDC()

        circ_pump_2 = ElectricDriveDC(**data_for_driver)
        circ_pump_2.name = "Циркуляционный насос №2"
        circ_pump_2.work = False
        circ_pump_2.stop = True
        circ_pump_2.is_frequency_converter = True
        circ_pump_2.frequency_converter = FrequencyConverterDC()

        circulation_pumps = PumpGroupControlModeDC(
            name="Циркуляционные насосы",
            is_automatic=True,
            electric_drivers=[circ_pump_1, circ_pump_2]
        )

        hot_water_pump = ElectricDriveDC(**data_for_driver)
        hot_water_pump.name = "Насос горячей воды"

        object_heat_point = TelemetryHeatPointNamedDC(
            name=RegisteredObjects.HEAT_POINT_CENTER.value[0],
            pump_groups=[circulation_pumps],
            pumps=[hot_water_pump],
            **data_heat_point
        )

        data_from_connector: dict = {heat_point_name: object_heat_point.model_dump()}
        serializer = TelemetrySerializer(data=data_from_connector)

        assert serializer.is_valid(raise_exception=True) is True

        data: dict = serializer.data["heat_point_center"]
        assert len(data) == 17
        assert len(data["pump_groups"]) == 1
        assert len(data["pumps"]) == 1


import pytest
from typing import Callable
from rest_framework.exceptions import ValidationError

from sensors.serializers.serializers import TimeSpentStateSerializer, ElectricDriveSerializer, \
    FloodMonitoringSerializer, IllegalAccessSerializer, PressureMaintenanceMonitoringSerializer, \
    PowerSupplyMonitoringSerializer, PumpGroupControlModeSerializer
from ..structures import ElectricDriveDC, FrequencyConverterDC, AlarmSituationDC, PumpGroupControlModeDC


class TestTimeSpentStateSerializer:

    @pytest.mark.parametrize("value, expected", [(0, "00:00:00:00"), (110, "00:00:01:50"), (86410, "01:00:00:10")])
    def test_validate_data(self, value, expected):
        data = {"quantity_seconds": value}
        serializer = TimeSpentStateSerializer(data=data)

        assert serializer.is_valid(raise_exception=True) is True
        serializer_data: dict = serializer.data

        assert len(serializer_data) == 1
        assert isinstance(serializer_data["time_spent"], str)
        assert serializer_data["time_spent"] == expected

    def test_not_validate_data(self):
        data = {"quantity_seconds": -10}
        with pytest.raises(ValidationError):
            serializer = TimeSpentStateSerializer(data=data)
            serializer.is_valid(raise_exception=True)


class TestElectricDriveSerializer:
    electric_drive = ElectricDriveDC(
        name="Циркуляционный насос №1",
        work=True,
        stop=False,
        alarm=False,
        operating_time=8,
        is_frequency_converter=False
    )
    frequency_converter = FrequencyConverterDC(alarm=False)

    def test_validate_data(self):
        serializer = ElectricDriveSerializer(data=self.electric_drive.model_dump())
        assert serializer.is_valid(raise_exception=True) is True

        # Добавляем вложенный ЧП
        electric_drive = ElectricDriveDC(**self.electric_drive.model_dump())
        electric_drive.is_frequency_converter = True
        electric_drive.frequency_converter = self.frequency_converter

        serializer = ElectricDriveSerializer(data=electric_drive.model_dump())
        assert serializer.is_valid(raise_exception=True) is True

        serializer_data: dict = serializer.data
        assert len(serializer_data) == 7

    def test_not_validate_data(self):
        """ Тестируется доп. проверка в методе 'validate' """

        self.electric_drive.frequency_converter = self.frequency_converter
        serializer = ElectricDriveSerializer(data=self.electric_drive.model_dump())

        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        assert "Поле должно быть True" in str(exc_info.value)


class TestPumpGroupControlModeSerializer:

    def test_validate_data(self, data_for_driver):
        driver_1 = ElectricDriveDC(**data_for_driver)
        driver_2 = ElectricDriveDC(**data_for_driver)
        driver_2.name = "Циркуляционный насос №2"
        driver_2.work = False
        driver_2.stop = True

        circulation_pumps = PumpGroupControlModeDC(
            name="Циркуляционные насосы",
            is_automatic=True,
            electric_drivers=[driver_1, driver_2]
        )
        serializer = PumpGroupControlModeSerializer(data=circulation_pumps.model_dump())
        assert serializer.is_valid(raise_exception=True) is True

        data: dict = serializer.data
        assert len(data) == 3

    def test_not_validate_data(self):
        """ Список насосов в группе не должен быть пустым """

        circulation_pumps = PumpGroupControlModeDC(
            name="Циркуляционные насосы",
            is_automatic=True
        )
        serializer = PumpGroupControlModeSerializer(data=circulation_pumps.model_dump())
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        assert "Список не должен быть пустым" in str(exc_info.value)


class TestAlarmSerializers:

    ALARMS: tuple[Callable] = (
        FloodMonitoringSerializer,
        IllegalAccessSerializer,
        PowerSupplyMonitoringSerializer,
        PressureMaintenanceMonitoringSerializer
    )

    @pytest.mark.parametrize("alarm", [*ALARMS])
    def test_alarms_validate_data(self, alarm):
        alarm_signal = AlarmSituationDC(alarm=True, quantity_seconds=10)
        serializer = alarm(data=alarm_signal.model_dump())

        assert serializer.is_valid(raise_exception=True) is True

        data = serializer.data
        assert len(data) == 3
        assert data.get("name") is not None
        assert data.get("alarm") is not None
        assert data.get("time_spent") is not None

    @pytest.mark.parametrize("alarm", [*ALARMS])
    def test_alarms_not_validate_data(self, alarm):
        """ Seconds should be positive numbers. """

        alarm_signal = AlarmSituationDC(alarm=True, quantity_seconds=-2)

        with pytest.raises(ValidationError):
            serializer = alarm(data=alarm_signal.model_dump())
            serializer.is_valid(raise_exception=True)


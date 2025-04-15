import pytest
from rest_framework.exceptions import ValidationError

from ..serializers import TimeSpentStateSerializer, ElectricDriveSerializer
from ..structures import ElectricDriveDC, FrequencyConverterDC


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


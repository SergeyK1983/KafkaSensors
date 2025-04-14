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

    def test_validate_data(self):
        electric_drive = ElectricDriveDC(
            name="Циркуляционный насос №1",
            work=True,
            stop=False,
            alarm=False,
            operating_time=8,
            is_frequency_converter=False
        )
        serializer = ElectricDriveSerializer(data=electric_drive.model_dump())
        assert serializer.is_valid(raise_exception=True) is True

    def test_not_validate_data(self):
        frequency_converter = FrequencyConverterDC(alarm=False)
        electric_drive = ElectricDriveDC(
            name="Циркуляционный насос №1",
            work=True,
            stop=False,
            alarm=False,
            operating_time=8,
            is_frequency_converter=False,
            frequency_converter=frequency_converter
        )
        with pytest.raises(ValidationError) as exc_info:
            serializer = TimeSpentStateSerializer(data=electric_drive.model_dump())
            serializer.is_valid(raise_exception=True)


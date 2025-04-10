from django.core.validators import MinValueValidator
from rest_framework import serializers


class FrequencyConverterSerializer(serializers.Serializer):
    alarm = serializers.BooleanField(default=False, help_text="Тревога/Авария")


class ElectricDriveSerializer(serializers.Serializer):
    """ Состояние электропривода """

    name = serializers.CharField(max_length=50, help_text="Наименование")
    work = serializers.BooleanField(help_text="В работе")
    stop = serializers.BooleanField(help_text="Остановлен")
    alarm = serializers.BooleanField(default=False, help_text="Тревога/Авария")
    operating_time = serializers.IntegerField(
        validators=[MinValueValidator(0)], required=False, allow_null=True, help_text="Время наработки, в часах"
    )
    is_frequency_converter = serializers.BooleanField(default=False, help_text="Наличие ЧП")
    frequency_converter = FrequencyConverterSerializer(required=False, many=False)

    def validate_is_frequency_converter(self, attrs):
        if attrs["frequency_converter"]:
            if not attrs["is_frequency_converter"]:
                raise serializers.ValidationError(f"Поле 'is_frequency_converter' должно быть True")


class PumpGroupControlMode(serializers.Serializer):
    """ Группа насосов, режим работы """

    name = serializers.CharField(max_length=50, help_text="Наименование")
    is_automatic = serializers.BooleanField(help_text="Автоматическое управление")
    electric_drivers = ElectricDriveSerializer(many=True)


class TelemetryHeatPointSerializer(serializers.Serializer):
    """ Телеметрия теплового пункта """
    pass


class TelemetrySerializer(serializers.Serializer):
    """ Телеметрия """
    pass


OBJECTS_TELEMETRY = {
    "heat_point": TelemetryHeatPointSerializer,
}


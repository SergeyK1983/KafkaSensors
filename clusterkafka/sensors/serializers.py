from django.core.validators import MinValueValidator, MaxValueValidator
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
        validators=[MinValueValidator(0), MaxValueValidator(100000)], required=False, allow_null=True,
        help_text="Время наработки, в часах"
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

    pressure_supply_pipeline_heating_input = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(1600.00)],
        help_text="Давление в подающем трубопроводе ТС, вход, кПа"
    )
    pressure_return_pipeline_heating_input = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(1600.00)],
        help_text="Давление в обратном трубопроводе ТС, вход, кПа"
    )
    temperature_supply_pipeline_heating_input = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(200.00)],
        help_text="Температура в подающем трубопроводе ТС, вход, С"
    )
    temperature_return_pipeline_heating_input = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(200.00)],
        help_text="Температура в обратном трубопроводе ТС, вход, С"
    )
    outdoor_air_temperature = serializers.FloatField(
        validators=[MinValueValidator(-60.00), MaxValueValidator(60.00)],
        help_text="Температура наружного воздуха, С"
    )
    pressure_supply_pipeline_heating_output = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(1600.00)],
        help_text="Давление в подающем трубопроводе ТС, выход, кПа"
    )
    pressure_return_pipeline_heating_output = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(1600.00)],
        help_text="Давление в обратном трубопроводе ТС, выход, кПа"
    )
    temperature_supply_pipeline_heating_output = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(200.00)],
        help_text="Температура в подающем трубопроводе ТС, выход, С"
    )
    temperature_return_pipeline_heating_output = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(200.00)],
        help_text="Температура в обратном трубопроводе ТС, выход, С"
    )


class TelemetrySerializer(serializers.Serializer):
    """ Телеметрия """
    pass


OBJECTS_TELEMETRY = {
    "heat_point": TelemetryHeatPointSerializer,
}


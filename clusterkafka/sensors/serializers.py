from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers


class FrequencyConverterSerializer(serializers.Serializer):
    """ Частотный преобразователь """

    alarm = serializers.BooleanField(default=False, help_text="Тревога/Авария")


class ElectricDriveSerializer(serializers.Serializer):
    """ Состояние электропривода """

    name = serializers.CharField(max_length=50, help_text="Наименование")
    work = serializers.BooleanField(help_text="В работе")
    stop = serializers.BooleanField(help_text="Остановлен")
    alarm = serializers.BooleanField(default=False, help_text="Тревога/Авария")
    operating_time = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        required=False,
        allow_null=True,
        help_text="Время наработки, в часах"
    )
    is_frequency_converter = serializers.BooleanField(default=False, help_text="Наличие ЧП")
    frequency_converter = FrequencyConverterSerializer(required=False, allow_null=True, many=False)

    def validate(self, data):
        if data["frequency_converter"] and not data["is_frequency_converter"]:
            msg = {"is_frequency_converter": "Поле должно быть True"}
            raise serializers.ValidationError(msg)

        return data


class PumpGroupControlModeSerializer(serializers.Serializer):
    """ Группа насосов, режим работы """

    name = serializers.CharField(max_length=50, help_text="Наименование")
    is_automatic = serializers.BooleanField(help_text="Автоматическое управление")
    electric_drivers = ElectricDriveSerializer(many=True)


class TimeSpentStateSerializer(serializers.Serializer):
    """ Время пребывания в состоянии. Входное значение - количество секунд. """

    quantity_seconds = serializers.IntegerField(
        validators=[MinValueValidator(0)], write_only=True, help_text="Пройденное время, в секундах"
    )
    time_spent = serializers.SerializerMethodField()

    def get_time_spent(self, obj) -> str:
        seconds: int = obj["quantity_seconds"]
        days: int = seconds // 86400
        hours: int = seconds % 86400 // 3600
        minutes: int = seconds % 3600 // 60
        seconds: int = seconds % 60
        time_spent: str = f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
        return time_spent


class FloodMonitoringSerializer(TimeSpentStateSerializer, serializers.Serializer):
    """ Контроль затопления. В т.ч. время пребывания в состоянии True. """

    is_flood = serializers.BooleanField(default=False, help_text="Затопление")


class IllegalAccessSerializer(TimeSpentStateSerializer, serializers.Serializer):
    """ Открытие дверей. Несанкционированный доступ. В т.ч. время пребывания в состоянии True. """

    door_is_open = serializers.BooleanField(default=False, help_text="Открытие дверей")


class PowerSupplyMonitoringSerializer(TimeSpentStateSerializer, serializers.Serializer):
    """ Контроль наличия напряжения на вводе. True если авария. В т.ч. время пребывания в состоянии True. """

    is_power_failure = serializers.BooleanField(default=False, help_text="Авария электропитания")


class PressureMaintenanceMonitoringSerializer(TimeSpentStateSerializer, serializers.Serializer):
    """ Контроль работы установок поддержания давления. True если авария. В т.ч. время пребывания в состоянии True. """

    is_pressure_maintenance_failure = serializers.BooleanField(
        default=False, help_text="Авария установок поддержания давления"
    )


class HeatMeterSerializer(serializers.Serializer):
    """ Теплосчетчик с часовыми показателями. Учетные показатели с нарастающим итогом. """

    time_created_seconds = serializers.DateTimeField(
        required=False,
        help_text="Время архивирования"
    )
    mass_consumption_supply = serializers.FloatField(
        validators=[MinValueValidator(0.0000)],
        help_text="Массовый расход теплоносителя подающий, т"
    )
    mass_consumption_return = serializers.FloatField(
        validators=[MinValueValidator(0.0000)],
        help_text="Массовый расход теплоносителя обратный, т"
    )
    mass_consumption_replenish = serializers.FloatField(
        required=False,
        validators=[MinValueValidator(0.0000)],
        help_text="Массовый расход теплоносителя подпитка, т"
    )
    consumption_replenish = serializers.FloatField(
        required=False,
        validators=[MinValueValidator(0.0000)],
        help_text="Расход воды, подпитка, м3"
    )
    heat_energy_consumption = serializers.FloatField(
        validators=[MinValueValidator(0.0000)],
        help_text="Расход тепловой энергии, Гкал"
    )
    temperature_supply_pipeline = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(200.00)],
        help_text="Температура в подающем трубопроводе ТС, С"
    )
    temperature_return_pipeline = serializers.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(200.00)],
        help_text="Температура в обратном трубопроводе ТС, С"
    )
    pressure_supply_pipeline = serializers.FloatField(
        required=False,
        validators=[MinValueValidator(0.000), MaxValueValidator(1.600)],
        help_text="Давление в подающем трубопроводе ТС, МПа"
    )
    pressure_return_pipeline = serializers.FloatField(
        required=False,
        validators=[MinValueValidator(0.000), MaxValueValidator(1.600)],
        help_text="Давление в обратном трубопроводе ТС, МПа"
    )
    time_normal_mode = serializers.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Чистое время работы в нормальном режиме, мин."
    )
    time_error_mode = serializers.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Общее время простоя, мин."
    )
    checksum = serializers.IntegerField(help_text="Контрольная сумма")


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
    power_input_main = PowerSupplyMonitoringSerializer(many=False)
    power_input_reserve = PowerSupplyMonitoringSerializer(many=False)


class TelemetrySerializer(serializers.Serializer):
    """ Телеметрия """
    pass


OBJECTS_TELEMETRY = {
    "heat_point": TelemetryHeatPointSerializer,
}


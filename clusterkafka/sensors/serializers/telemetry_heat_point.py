from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from sensors.serializers.serializers import PowerSupplyMonitoringSerializer, PressureMaintenanceMonitoringSerializer, \
    IllegalAccessSerializer, FloodMonitoringSerializer


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
    power_input_main = PowerSupplyMonitoringSerializer(many=False, help_text="Основной ввод электропитания ИТП")
    power_input_reserve = PowerSupplyMonitoringSerializer(many=False, help_text="Резервный ввод электропитания ИТП")
    pressure_maintenance = PressureMaintenanceMonitoringSerializer(many=False)
    illegal_access = IllegalAccessSerializer(many=False)
    flood_monitoring = FloodMonitoringSerializer(many=False)


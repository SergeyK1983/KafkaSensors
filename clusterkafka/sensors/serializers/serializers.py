from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from sensors.constants import AlarmSignalsHeatPoint


class AlarmSignalMixin(serializers.Serializer):
    """ Аварийный сигнал (общий) """

    alarm = serializers.BooleanField(default=False, help_text="Тревога/Авария")


class FrequencyConverterSerializer(AlarmSignalMixin):
    """ Частотный преобразователь """

    pass


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

    def validate_electric_drivers(self, value):
        if not value:
            msg = {"electric_drivers": "Список не должен быть пустым"}
            raise serializers.ValidationError(msg)

        return value


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


class FloodMonitoringSerializer(AlarmSignalMixin, TimeSpentStateSerializer):
    """ Контроль затопления. В т.ч. время пребывания в состоянии True. """

    name = serializers.CharField(default=AlarmSignalsHeatPoint.is_flood.value, read_only=True)


class IllegalAccessSerializer(AlarmSignalMixin, TimeSpentStateSerializer):
    """ Открытие дверей. Несанкционированный доступ. В т.ч. время пребывания в состоянии True. """

    name = serializers.CharField(default=AlarmSignalsHeatPoint.door_is_open.value, read_only=True)


class PowerSupplyMonitoringSerializer(AlarmSignalMixin, TimeSpentStateSerializer):
    """ Контроль наличия напряжения на вводе. True если авария. В т.ч. время пребывания в состоянии True. """

    name = serializers.CharField(default=AlarmSignalsHeatPoint.is_power_failure.value, read_only=True)


class PressureMaintenanceMonitoringSerializer(AlarmSignalMixin, TimeSpentStateSerializer):
    """ Контроль работы установок поддержания давления. True если авария. В т.ч. время пребывания в состоянии True. """

    name = serializers.CharField(default=AlarmSignalsHeatPoint.is_pressure_maintenance_failure.value, read_only=True)


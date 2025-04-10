from rest_framework import serializers


class ElectricDriveSerializer(serializers.Serializer):
    """ Состояние электропривода """

    name = serializers.CharField(max_length=50)
    work = serializers.BooleanField()
    stop = serializers.BooleanField()
    alarm = serializers.BooleanField()


class PumpGroupControlMode(serializers.Serializer):
    """ Режим работы группы насосов """

    is_automatic = serializers.BooleanField()
    electric_drivers = ElectricDriveSerializer(many=True)


class TelemetryHeatPointSerializer(serializers.Serializer):
    """ Телеметрия теплового пункта """
    pass


class TelemetrySerializer(serializers.Serializer):
    """ Телеметрия """
    pass


OBJECT_TELEMETRY = {
    "heat_point": TelemetryHeatPointSerializer,
}


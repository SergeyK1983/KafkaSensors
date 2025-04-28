from enum import Enum


class RegisteredObjects(Enum):
    """
    Зарегистрированные объекты для телеметрии.
    value = ("Наименование", "ключ для OBJECTS_TELEMETRY")
    """

    HEAT_POINT_CENTER = ("ИТП \"Центральный\"", "heat_point")
    HEAT_METER_CENTER = ("ИТП \"Центральный\" Тепловой учет", "heat_meter")


class AlarmSignalsHeatPoint(Enum):
    """ Аварийные сигналы теплового пункта """

    is_flood = "Затопление"
    door_is_open = "Несанкционированный доступ"
    is_power_failure = "Авария электропитания"
    is_pressure_maintenance_failure = "Авария установок поддержания давления"


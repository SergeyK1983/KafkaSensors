from enum import Enum


class AlarmSignalsHeatPoint(Enum):
    """ Аварийные сигналы теплового пункта """

    is_flood = "Затопление"
    door_is_open = "Несанкционированный доступ"
    is_power_failure = "Авария электропитания"
    is_pressure_maintenance_failure = "Авария установок поддержания давления"


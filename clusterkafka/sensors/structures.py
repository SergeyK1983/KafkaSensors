from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class CommonBaseMethods:

    def model_dump(self) -> dict:
        return asdict(self)

    def list_fields(self) -> list:
        attrs: list[str] = list(asdict(self).keys())
        return attrs


@dataclass
class FrequencyConverterDC:
    """ Частотный преобразователь """

    alarm: bool = False


@dataclass
class ElectricDriveDC(CommonBaseMethods):
    """ Состояние электропривода """

    name: str
    work: bool
    stop: bool
    alarm: bool
    operating_time: int | None
    is_frequency_converter: bool = False
    frequency_converter: FrequencyConverterDC | None = None


@dataclass
class PumpGroupControlModeDC(CommonBaseMethods):
    """ Группа насосов, режим работы """

    name: str
    is_automatic: bool
    electric_drivers: list[ElectricDriveDC] = field(default_factory=list)


@dataclass
class AlarmSituationDC(CommonBaseMethods):
    """ Аварийная ситуация, аварийный режим """

    alarm: bool = False
    quantity_seconds: int = 0


@dataclass
class TelemetryHeatMeterNamedDC(CommonBaseMethods):
    """ Учет тепловой энергии. TelemetryHeatMeterNamedSerializer. """

    name: str
    time_created_seconds: str | datetime | None
    mass_consumption_supply: float
    mass_consumption_return: float
    mass_consumption_replenish: float | None
    consumption_replenish: float | None
    heat_energy_consumption: float
    temperature_supply_pipeline: float
    temperature_return_pipeline: float
    pressure_supply_pipeline: float | None
    pressure_return_pipeline: float | None
    time_normal_mode: int
    time_error_mode: int
    checksum: int


@dataclass
class TelemetryHeatPointNamedDC(CommonBaseMethods):
    """ Телеметрия теплового пункта. TelemetryHeatPointNamedSerializer. """

    name: str
    pressure_supply_pipeline_heating_input: float
    pressure_return_pipeline_heating_input: float
    temperature_supply_pipeline_heating_input: float
    temperature_return_pipeline_heating_input: float
    outdoor_air_temperature: float
    pressure_supply_pipeline_heating_output: float
    pressure_return_pipeline_heating_output: float
    temperature_supply_pipeline_heating_output: float
    temperature_return_pipeline_heating_output: float
    power_input_main: AlarmSituationDC
    power_input_reserve: AlarmSituationDC
    pressure_maintenance: AlarmSituationDC
    illegal_access: AlarmSituationDC
    flood_monitoring: AlarmSituationDC
    pump_groups: list[PumpGroupControlModeDC] | None = None
    pumps: list[ElectricDriveDC] | None = None


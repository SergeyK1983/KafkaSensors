from dataclasses import dataclass, field, asdict


@dataclass
class CommonBaseMethods:

    def model_dump(self) -> dict:
        return asdict(self)


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

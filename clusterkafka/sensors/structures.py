from dataclasses import dataclass


class FrequencyConverterDC(dataclass):
    """ Частотный преобразователь """

    alarm: bool = False


class ElectricDriveDC(dataclass):
    """ Состояние электропривода """

    name: str = ""
    work: bool
    stop: bool
    alarm: bool = False
    operating_time: int
    is_frequency_converter: bool
    frequency_converter: FrequencyConverterDC | None = None


class PumpGroupControlModeDC(dataclass):
    """ Группа насосов, режим работы """

    name: str = ""
    is_automatic: bool
    electric_drivers: list[ElectricDriveDC]


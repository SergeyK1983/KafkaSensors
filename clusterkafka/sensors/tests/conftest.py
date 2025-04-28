import pytest
from datetime import datetime

from sensors.structures import AlarmSituationDC


@pytest.fixture
def data_for_driver() -> dict:
    """
    Структура телеметрии электропривода. Начальные данные: name="Насос 1", work=True, stop=False, alarm=False,
    operating_time=8, is_frequency_converter=False.
    :return: данные для ElectricDriveDC
    """
    driver = {
        "name": "Циркуляционный насос №1",
        "work": True,
        "stop": False,
        "alarm": False,
        "operating_time": 8,
        "is_frequency_converter": False
    }
    return driver


@pytest.fixture
def data_for_heat_meter() -> dict:
    """
    Структура телеметрии теплового учета.
    :return: Данные для TelemetryHeatMeterNamedSerializer.
    """
    data = {
        # "name": "Учет тепловой энергии ИТП №1",
        "time_created_seconds": datetime.now(),
        "mass_consumption_supply": 0.12,
        "mass_consumption_return": 0.11,
        "mass_consumption_replenish": 0.01,
        "consumption_replenish": 10.01,
        "heat_energy_consumption": 0.365,
        "temperature_supply_pipeline": 105.3,
        "temperature_return_pipeline": 72.2,
        "pressure_supply_pipeline": 0.92,
        "pressure_return_pipeline": 0.88,
        "time_normal_mode": 60,
        "time_error_mode": 0,
        "checksum": 12365
    }
    return data


@pytest.fixture
def data_for_heat_point() -> dict:
    data: dict = {
        # name = "ИТП №1",
        "pressure_supply_pipeline_heating_input": 852.23,
        "pressure_return_pipeline_heating_input": 800.37,
        "temperature_supply_pipeline_heating_input": 104.33,
        "temperature_return_pipeline_heating_input": 75.63,
        "outdoor_air_temperature": -24.5,
        "pressure_supply_pipeline_heating_output": 849.3,
        "pressure_return_pipeline_heating_output": 800.75,
        "temperature_supply_pipeline_heating_output": 90.5,
        "temperature_return_pipeline_heating_output": 71.6,
        "power_input_main": AlarmSituationDC(),
        "power_input_reserve": AlarmSituationDC(),
        "pressure_maintenance": AlarmSituationDC(),
        "illegal_access": AlarmSituationDC(),
        "flood_monitoring": AlarmSituationDC()
    }
    return data

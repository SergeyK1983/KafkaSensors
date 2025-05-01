from datetime import datetime
from random import random, randint, uniform

from sensors.constants import RegisteredObjects
from sensors.structures import HeatMeterNamedDC, TelemetryHeatPointNamedDC, PumpGroupControlModeDC, ElectricDriveDC, \
    AlarmSituationDC, FrequencyConverterDC


class FakeHeatMeterCenter:

    @classmethod
    def input_data(cls) -> HeatMeterNamedDC:
        data = HeatMeterNamedDC(
            name=RegisteredObjects.HEAT_METER_CENTER.value[0],
            time_created_seconds=datetime.now(),
            mass_consumption_supply=round(random(), 4),
            mass_consumption_return=round(random(), 4),
            mass_consumption_replenish=round(random(), 4),
            consumption_replenish=round(uniform(0, 20), 4),
            heat_energy_consumption=round(uniform(0, 10), 4),
            temperature_supply_pipeline=round(uniform(100, 105), 2),
            temperature_return_pipeline=round(uniform(70, 75), 2),
            pressure_supply_pipeline=round(uniform(0.8, 1.1), 3),
            pressure_return_pipeline=round(uniform(0.8, 1.1), 3),
            time_normal_mode=60,
            time_error_mode=0,
            checksum=randint(1000, 9999)
        )
        return data


class FakeHeatPointCenter:

    @classmethod
    def input_data(cls) -> TelemetryHeatPointNamedDC:
        circ_pump_1 = ElectricDriveDC(
            name="Циркуляционный насос №1",
            work=True,
            stop=False,
            alarm=False,
            operating_time=8,
            is_frequency_converter=True,
            frequency_converter=FrequencyConverterDC()
        )
        circ_pump_2 = ElectricDriveDC(
            name="Циркуляционный насос №2",
            work=False,
            stop=True,
            alarm=False,
            operating_time=8,
            is_frequency_converter=True,
            frequency_converter=FrequencyConverterDC()
        )

        circulation_pumps = PumpGroupControlModeDC(
            name="Циркуляционные насосы",
            is_automatic=True,
            electric_drivers=[circ_pump_1, circ_pump_2]
        )
        hot_water_pump = ElectricDriveDC(
            name="Насос горячей воды",
            work=True,
            stop=False,
            alarm=False,
            operating_time=8,
            is_frequency_converter=False
        )

        data = TelemetryHeatPointNamedDC(
            name=RegisteredObjects.HEAT_POINT_CENTER.value[0],
            pressure_supply_pipeline_heating_input=round(uniform(700, 990), 2),
            pressure_return_pipeline_heating_input=round(uniform(700, 990), 2),
            temperature_supply_pipeline_heating_input=round(uniform(100, 105), 2),
            temperature_return_pipeline_heating_input=round(uniform(70, 75), 2),
            outdoor_air_temperature=round(uniform(-30, 0), 2),
            pressure_supply_pipeline_heating_output=round(uniform(700, 990), 2),
            pressure_return_pipeline_heating_output=round(uniform(700, 990), 2),
            temperature_supply_pipeline_heating_output=round(uniform(90, 95), 2),
            temperature_return_pipeline_heating_output=round(uniform(70, 75), 2),
            power_input_main=AlarmSituationDC(),
            power_input_reserve=AlarmSituationDC(),
            pressure_maintenance=AlarmSituationDC(),
            illegal_access=AlarmSituationDC(),
            flood_monitoring=AlarmSituationDC(),
            pump_groups=[circulation_pumps],
            pumps=[hot_water_pump]
        )
        return data

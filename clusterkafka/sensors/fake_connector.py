from datetime import datetime
from random import random, randint, uniform

from sensors.constants import RegisteredObjects
from sensors.structures import HeatMeterNamedDC


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

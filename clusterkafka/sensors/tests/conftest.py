import pytest


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


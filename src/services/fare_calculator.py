import abc

from calendar import SUNDAY
from datetime import datetime


class FareCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate(distance: float) -> float:
        ...


class FareCalculatorFactory:
    def __init__(self, date: datetime) -> None:
        date = datetime.fromisoformat(date)
        if date.weekday() == SUNDAY:
            self._calc = SundayFare()
        elif date.hour < 8 or date.hour > 18:
            self._calc = OvernightFare()
        elif date.hour >= 8 and date.hour <= 18:
            self._calc = NormalFare()

    def calculate(self, distance) -> float:
        return self._calc.calculate(distance=distance)


class SundayFare(FareCalculator):
    def calculate(self, distance: float) -> float:
        tariff = 5
        return distance * tariff


class OvernightFare(FareCalculator):
    def calculate(self, distance: float) -> float:
        tariff = 3.9
        return distance * tariff


class NormalFare(FareCalculator):
    def calculate(self, distance: float) -> float:
        tariff = 2.1
        return distance * tariff

import re

from src.presenter import ErrorInvalidCpf


class CpfObject:
    def __init__(self, cpf) -> None:
        self.CPF_LENGTH = 11
        self.FACTOR_FIRST_DIGIT = 10
        self.FACTOR_SECOND_DIGIT = 11
        if not self._validate(raw_cpf=cpf):
            raise ErrorInvalidCpf()
        self._value = self._get_only_numbers(value=cpf)

    def get_value(self) -> str:
        return self._value

    def _validate(self, raw_cpf: str):
        if not raw_cpf:
            return False
        cpf = self._get_only_numbers(value=raw_cpf)
        if len(cpf) != self.CPF_LENGTH:
            return False
        if self._all_digits_the_same(value=cpf):
            return False
        first_digit = self._calculate_digit(cpf=cpf, factor=self.FACTOR_FIRST_DIGIT)
        second_digit = self._calculate_digit(cpf=cpf, factor=self.FACTOR_SECOND_DIGIT)
        return self._get_actual_digit(cpf=cpf) == f"{first_digit}{second_digit}"

    def _get_only_numbers(self, value: str) -> str:
        return re.sub("\D", "", value)  # noqa: W605

    def _all_digits_the_same(self, value: str) -> bool:
        firstDigit = value[0]
        return all(digit == firstDigit for digit in value)

    def _calculate_digit(self, cpf: str, factor: int):
        total = 0
        for digit in cpf:
            if factor > 1:
                total += int(digit) * factor
                factor -= 1
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    def _get_actual_digit(self, cpf: str):
        return cpf[-2:]

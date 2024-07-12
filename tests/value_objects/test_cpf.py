import pytest

from src.domain.value_objects import CpfObject
from src.presenter import ErrorInvalidCpf


def test_invalid_cpf_all_digits_are_same():
    with pytest.raises(ErrorInvalidCpf):
        cpf = "111.111.111-11"
        CpfObject(cpf).get_value()


def test_invalid_cpf_less_digits():
    with pytest.raises(ErrorInvalidCpf):
        cpf = "111.111.111"
        CpfObject(cpf).get_value()


def test_invalid_cpf_more_digits():
    with pytest.raises(ErrorInvalidCpf):
        cpf = "111.111.111-111"
        CpfObject(cpf).get_value()


def test_invalid_cpf_letters():
    with pytest.raises(ErrorInvalidCpf):
        cpf = "111.111.111-ab"
        CpfObject(cpf).get_value()


def test_valid_cpf():
    cpf = "857.306.180-42"
    value_cpf = CpfObject(cpf).get_value()
    assert value_cpf == cpf.replace(".", "").replace("-", "")


def test_valid_cpf_without_mask():
    cpf = "85730618042"
    value_cpf = CpfObject(cpf).get_value()
    assert value_cpf == cpf

import pytest

from src.domain.value_objects import CpfObject
from src.presenter import ErrorInvalidCpf


@pytest.mark.parametrize("cpf_input", ["111.111.111-11", "857.306.180", "857.306.180-421", "857.306.180-ab"])
def test_invalid_cpf(cpf_input):
    with pytest.raises(ErrorInvalidCpf):
        CpfObject(cpf_input).get_value()


@pytest.mark.parametrize("cpf_input", ["857.306.180-42", "85730618042"])
def test_valid_cpf(cpf_input):
    value_cpf = CpfObject(cpf_input).get_value()
    assert value_cpf == cpf_input.replace(".", "").replace("-", "")

import abc

from src.presenter import ErrorIsInvalidUUID
from src.utils import Validates


class BaseUseCase(abc.ABC):
    def __init__(self) -> None:
        self._validate = Validates()

    @abc.abstractmethod
    def run(self):
        ...

    def _validate_id(self, id: str):
        if not self._validate.is_uuid(id=id):
            raise ErrorIsInvalidUUID()

    def _validate_list_id(self, list_id: list[str]):
        for id in list_id:
            self._validate_id(id=id)


class BaseGetUseCase:
    def __init__(self) -> None:
        self._validate = Validates()

    @abc.abstractmethod
    def get_id(self, id):
        if not self._validate.is_uuid(id=id):
            raise ErrorIsInvalidUUID()

import abc
from src.presenter import ErrorIsInvalidUUID
from src.addapters.validate import is_uuid

class BaseUseCase(abc.ABC):
    @abc.abstractmethod
    def run(self):
        ...

    def _validate_id(self, id: str):
        if not is_uuid(id=id):
            raise ErrorIsInvalidUUID()

    def _validate_list_id(self, list_id: list[str]):
        for id in list_id:
            self._validate_id(id=id)

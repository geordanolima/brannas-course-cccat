from src.addapters.validate import is_uuid
from src.presenter import ErrorIsInvalidUUID


class BaseGetUseCase:
    def get_id(self, id):
        if not is_uuid(id=id):
            raise ErrorIsInvalidUUID()

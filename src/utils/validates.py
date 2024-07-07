import uuid


class Validates:
    def is_uuid(self, id: str):
        try:
            uuid.UUID(id)
            return True
        except Exception:
            return False

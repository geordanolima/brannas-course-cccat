from uuid import UUID


def is_uuid(id: str):
    try:
        UUID(id)
        return True
    except Exception:
        return False

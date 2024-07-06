import re
import uuid


class Validates:
    def invalid_name(self, name):
        return not re.search(r"[a-zA-Z] [a-zA-Z]+", name)

    def invalid_email(self, email):
        return not re.search(r"^(.+)@(.+)$", email)

    def invalid_plate(self, plate: str, is_driver: bool):
        if is_driver:
            plate = plate.replace("-", "")
            return not re.search(r"^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$", plate)
        return False

    def is_uuid(self, id: str):
        try:
            uuid.UUID(id)
            return True
        except:
            return False

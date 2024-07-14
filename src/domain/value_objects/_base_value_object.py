class BaseValueObject():
    def __init__(self) -> None:
        self.get_value = None

    def get_value(self):
        return self._value

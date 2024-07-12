from datetime import datetime


class BaseEntitie():
    def object(self):
        updated_values = {}
        for item in self._value:
            if isinstance(item[1], datetime):
                updated_values[item[0]] = item[1].isoformat()
            else:
                updated_values[item[0]] = item[1]
        return type(self._value)(**updated_values)


from enum import Enum


class MachineStatus:
    def __init__(self, machine_status: list[dict]) -> None:
        self._machine = machine_status

    def validate_next_status(self, current_status: Enum, new_status: Enum):
        return new_status in self._get_permitted_next_status(current_status=current_status)

    def _get_permitted_next_status(self, current_status):
        result = []
        for status in self._machine:
            if status.get("current_status").value == current_status:
                for permited_status in status.get("permitted_next_status", []):
                    result.append(permited_status.value)
        return result

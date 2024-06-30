from enum import Enum


class ValueConstructibleEnum(Enum):
    @classmethod
    def create_from_value(cls, value):
        for enum_choice in cls:
            if value == enum_choice.value:
                return enum_choice
        raise Exception(f"Enum does not have {value=}")


class RideStatusEnum(ValueConstructibleEnum):
    CREATED = 0
    CANCELED = 1
    ERROR = 2
    PENDING_ACCEPT = 3
    ACCEPT = 4
    IN_PROGRESS = 5
    PENDING_PAY = 6
    PAY_FAIL = 7
    PENDING_RATE = 8
    FINISHED = 9

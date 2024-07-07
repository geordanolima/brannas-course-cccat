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
    ACCEPT = 3
    IN_PROGRESS = 4
    PENDING_PAY = 5
    PAY_FAIL = 6
    PENDING_RATE = 7
    FINISHED = 8

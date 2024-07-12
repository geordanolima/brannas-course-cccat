from fastapi import status


class BaseException(Exception):
    message = None
    http_status = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=None, http_status=None, *args):
        self.message = message or self.message
        self.http_status = http_status or self.http_status
        super().__init__(self.message, *args)

    def response(self):
        return self.message, self.http_status


class ErrorAccountExistent(BaseException):
    message = {"ERROR": "ACCOUNT EXISTENT", "CODE": -4}
    http_status = status.HTTP_409_CONFLICT


class ErrorAccountNotFound(BaseException):
    message = {"ERROR": "ACCOUNT NOT FOUND"}
    http_status = status.HTTP_404_NOT_FOUND


class ErrorCoordinatesEquals(BaseException):
    message = {"ERROR": "COORDINATES ARE SAME"}


class ErrorCoordinateInvalid(BaseException):
    message = {
        "ERROR": "COORDINATE LATITUDE OR LONGITUDE INVALID",
        "VALIDATION": [
            "LATITUDE BETWEEN -90 AND 90",
            "LONGITUDE BETWEEN -180 AND 180",
        ]
    }


class ErrorHaveRideInProgress(BaseException):
    message = {"ERROR": "HAVE A RIDE IN PROGRESS"}


class ErrorInvalidCpf(BaseException):
    message = {"ERROR": "INVALID CPF", "CODE": -1}


class ErrorInvalidEmail(BaseException):
    message = {"ERROR": "INVALID EMAIL", "CODE": -2}


class ErrorInvalidName(BaseException):
    message = {"ERROR": "INVALID NAME", "CODE": -3}


class ErrorInvalidPlate(BaseException):
    message = {"ERROR": "INVALID PLATE", "CODE": -5}


class ErrorIsNeedDriver(BaseException):
    message = {"ERROR": "IS NEED DRIVER, TO EXECUTE THIS ACTION"}


class ErrorIsNeedPassenger(BaseException):
    message = {"ERROR": "IS NEED PASSENGER, TO EXECUTE THIS ACTION"}


class ErrorIsInvalidUUID(BaseException):
    message = {"ERROR": "ID INVALID"}


class ErrorLoginIncorrect(BaseException):
    message = {"ERROR": "LOGIN INCORRECT!"}
    http_status = status.HTTP_401_UNAUTHORIZED


class ErrorPasswordNotAccept(BaseException):
    message = {
        "ERROR": "PASSWORD NOT ACCEPT",
        "MESSAGE": "THE PASSWORD MUST BE BETWEEN 8 AND 16 CHARACTERS AND UPPERCASE AND LOWERCASE LETTERS AND NUMBERS"
    }


class ErrorRideInProgress(BaseException):
    message = {"ERROR": "RIDE IN PROGRESS"}


class ErrorRideNotFound(BaseException):
    message = {"ERROR": "RIDE NOT FOUND"}
    http_status = status.HTTP_404_NOT_FOUND


class ErrorRideOfOtherDriver(BaseException):
    message = {"ERROR": "RIDE OF OTHER DRIVER"}


class ErrorStatusNotAllowed(BaseException):
    message = {"ERROR": "STATUS NOT ALLOWED"}

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


class ErrorInvalidCpf(BaseException):
    message = {"ERROR": "INVALID CPF", "CODE": -1}


class ErrorInvalidEmail(BaseException):
    message = {"ERROR": "INVALID EMAIL", "CODE": -2}
    

class ErrorInvalidName(BaseException):
    message = {"ERROR": "INVALID NAME", "CODE": -3}


class ErrorAccountExistent(BaseException):
    message = {"ERROR": "ACCOUNT EXISTENT", "CODE": -4}
    http_status = status.HTTP_409_CONFLICT
    

class ErrorInvalidPlate(BaseException):
    message = {"ERROR": "INVALID PLATE", "CODE": -5}


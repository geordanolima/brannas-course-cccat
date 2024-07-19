import json

from fastapi import Response, status

from .errors import BaseException


class BasePresenter():
    def _general_response(self, body, status_code: int = status.HTTP_200_OK):
        return Response(json.dumps(body), status_code, media_type="application/Json")

    def response(self, body):
        return self._general_response(body)

    def response_error(self, error: BaseException):
        body, status_code = error.response()
        return self._general_response(body, status_code)

    def exception_handler(self, method, params):
        try:
            result = method(*params)
            return self.response(result.dict())
        except BaseException as error:
            return self.response_error(error)

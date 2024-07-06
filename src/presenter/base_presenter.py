import json

from fastapi import Response

from .errors import BaseException


class BasePresenter():
    def response(self, body):
        return Response(json.dumps(body), media_type="application/Json")

    def response_error(self, error: BaseException):
        body, status_code = error.response()
        return Response(json.dumps(body), status_code, media_type="application/Json")

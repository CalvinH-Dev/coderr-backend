from rest_framework.exceptions import APIException


class NotAuthorized(APIException):
    status_code = 401

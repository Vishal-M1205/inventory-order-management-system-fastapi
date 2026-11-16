from fastapi import status


class AppException(Exception):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class ConflictException(AppException):
    def __init__(self, detail, status_code=status.HTTP_409_CONFLICT):
        super().__init__(detail, status_code)

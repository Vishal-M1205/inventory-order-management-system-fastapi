from typing import Dict, Optional
from fastapi import status


class AppException(Exception):
    """Base application exception for all custom API exceptions."""

    def __init__(
        self,
        detail: str = "An unexpected error occurred.",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.headers = headers


class BadRequestException(AppException):
    """HTTP 400 Bad Request - Invalid request data or business rule failure."""

    def __init__(
        self,
        detail: str = "Bad request.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, headers)


class UnauthorizedException(AppException):
    """HTTP 401 Unauthorized - Missing or invalid authentication credentials."""

    def __init__(
        self,
        detail: str = "Could not validate credentials.",
        headers: Optional[Dict[str, str]] = None,
    ):
        auth_headers = {"WWW-Authenticate": "Bearer"}
        if headers:
            auth_headers.update(headers)
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED, auth_headers)


class InvalidCredentialsException(UnauthorizedException):
    """HTTP 401 Unauthorized - Incorrect email or password during login."""

    def __init__(
        self,
        detail: str = "Invalid email or password.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, headers)


class TokenExpiredException(UnauthorizedException):
    """HTTP 401 Unauthorized - Provided JWT token has expired."""

    def __init__(
        self,
        detail: str = "Token has expired.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, headers)


class InvalidTokenException(UnauthorizedException):
    """HTTP 401 Unauthorized - Provided JWT token is invalid or malformed."""

    def __init__(
        self,
        detail: str = "Invalid or malformed token.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, headers)


class ForbiddenException(AppException):
    """HTTP 403 Forbidden - Authenticated user lacks required permissions or scopes."""

    def __init__(
        self,
        detail: str = "You do not have permission to access this resource.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, status.HTTP_403_FORBIDDEN, headers)


class InactiveUserException(ForbiddenException):
    """HTTP 403 Forbidden - User account is deactivated."""

    def __init__(
        self,
        detail: str = "User account is inactive.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, headers)


class NotFoundException(AppException):
    """HTTP 404 Not Found - Requested resource does not exist."""

    def __init__(
        self,
        detail: str = "Resource not found.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, status.HTTP_404_NOT_FOUND, headers)


class ConflictException(AppException):
    """HTTP 409 Conflict - Resource already exists or conflicts with current state."""

    def __init__(
        self,
        detail: str = "Resource conflict.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, status.HTTP_409_CONFLICT, headers)


class UnprocessableEntityException(AppException):
    """HTTP 422 Unprocessable Entity - Semantic or business rule validation error."""

    def __init__(
        self,
        detail: str = "Unprocessable entity.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY, headers)


class InternalServerErrorException(AppException):
    """HTTP 500 Internal Server Error."""

    def __init__(
        self,
        detail: str = "An internal server error occurred.",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR, headers)

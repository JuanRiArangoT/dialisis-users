from fastapi import Request
from fastapi.responses import JSONResponse

from users.application.exceptions.user_exceptions import (
    UserConflictError,
    UserNotFoundApplicationError,
)


def user_conflict_exception_handler(
    request: Request,
    exc: UserConflictError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
        },
    )


def user_not_found_exception_handler(
    request: Request,
    exc: UserNotFoundApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": "User not found",
        },
    )

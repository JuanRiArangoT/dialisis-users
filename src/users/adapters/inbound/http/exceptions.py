from fastapi import Request
from fastapi.responses import JSONResponse

from users.application.exceptions.user_exceptions import UserConflictError


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

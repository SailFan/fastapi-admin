import traceback

from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
    ResponseValidationError,
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


class SettingNotFound(Exception):
    pass


async def DoesNotExistHandle(req: Request, exc: DoesNotExist) -> JSONResponse:
    print(f"[DoesNotExist] {exc}")
    print(traceback.format_exc())
    content = dict(
        code=404,
        msg=f"Object has not found, exc: {exc}, query_params: {req.query_params}",
    )
    return JSONResponse(content=content, status_code=404)


async def IntegrityHandle(_: Request, exc: IntegrityError) -> JSONResponse:
    print(f"[IntegrityError] {exc}")
    print(traceback.format_exc())
    content = dict(
        code=500,
        msg=f"IntegrityError，{exc}",
    )
    return JSONResponse(content=content, status_code=500)


async def HttpExcHandle(_: Request, exc: HTTPException) -> JSONResponse:
    print(f"[HTTPException] {exc.detail}")
    print(traceback.format_exc())
    content = dict(code=exc.status_code, msg=exc.detail, data=None)
    return JSONResponse(content=content, status_code=exc.status_code)


async def RequestValidationHandle(_: Request, exc: RequestValidationError) -> JSONResponse:
    print(f"[RequestValidationError] {exc}")
    print(traceback.format_exc())
    content = dict(code=422, msg=f"RequestValidationError, {exc}")
    return JSONResponse(content=content, status_code=422)


async def ResponseValidationHandle(_: Request, exc: ResponseValidationError) -> JSONResponse:
    print(f"[ResponseValidationError] {exc}")
    print(traceback.format_exc())
    content = dict(code=500, msg=f"ResponseValidationError, {exc}")
    return JSONResponse(content=content, status_code=500)


async def GeneralExceptionHandle(_: Request, exc: Exception) -> JSONResponse:
    """捕获所有未处理的异常"""
    print(f"[GeneralException] {type(exc).__name__}: {exc}")
    print(traceback.format_exc())
    content = dict(
        code=500,
        msg=f"Internal Server Error: {type(exc).__name__}: {str(exc)}",
    )
    return JSONResponse(content=content, status_code=500)

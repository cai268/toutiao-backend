import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# 开发模式：返回详细错误信息
# 生成模式：返回简化错误信息
DEBUG_MODE = True


def _error_response(
    status_code: int,
    message: str,
    detail: str | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    data = {"detail": detail} if DEBUG_MODE and detail else None # 开发者模式返回正确信息
    return JSONResponse(
        status_code=status_code,
        content={
            "code": status_code,
            "message": message,
            "data": data,
        },
        headers=headers,
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "请求处理失败"
    detail = None if isinstance(exc.detail, str) else str(exc.detail)
    return _error_response(
        status_code=exc.status_code,
        message=message,
        detail=detail,
        headers=exc.headers,
    )


async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message="数据完整性约束错误",
        detail=str(exc.orig),
    )


async def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="数据库操作失败",
        detail=str(exc),
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="服务器内部错误",
        detail=traceback.format_exc(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
        注册全局异常处理器,子类在前，父类在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler) # 业务
    app.add_exception_handler(IntegrityError, integrity_error_handler) # 数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler) # 数据库错误
    app.add_exception_handler(Exception, global_exception_handler) # 全局异常，兜底

from fastapi import APIRouter

from .field_def import router

field_def_router = APIRouter()
field_def_router.include_router(router, tags=["字段定义管理"])

__all__ = ["field_def_router"]

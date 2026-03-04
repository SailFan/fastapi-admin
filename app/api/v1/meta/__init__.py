from fastapi import APIRouter

from .meta import router

meta_router = APIRouter()
meta_router.include_router(router, tags=["元数据模块"])


__all__ = ["meta_router"]
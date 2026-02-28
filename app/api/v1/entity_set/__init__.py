from fastapi import APIRouter

from .entity_set import router

entity_set_router = APIRouter()
entity_set_router.include_router(router, tags=["实体集合管理"])

__all__ = ["entity_set_router"]

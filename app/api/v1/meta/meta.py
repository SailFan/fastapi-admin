from fastapi import Depends, APIRouter

from .registry  import (FIELD_TYPES,STRATEGIES,DISTRIBUTIONS,CONSTRAINT_TYPES)

router = APIRouter()


@router.get("/getmeta", summary="获取元数据")
async def get_meta():
    return {
        "field_types": FIELD_TYPES,
        "strategies": STRATEGIES,
        "distributions": DISTRIBUTIONS,
        "constraint_types": CONSTRAINT_TYPES
    }
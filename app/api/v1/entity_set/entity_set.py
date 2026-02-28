import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.entity_set import entity_set_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.entity_set import EntitySetCreate, EntitySetUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看实体集合列表")
async def list_entity_set(
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量"),
    name: str = Query(None, description="实体名称（模糊查询）"),
    category: str = Query(None, description="实体类别"),
):
    search = Q()
    if name:
        search &= Q(name__icontains=name)
    if category:
        search &= Q(category=category)
    
    total, entity_sets = await entity_set_controller.list(
        page=page,
        page_size=page_size,
        search=search,
        order=["-created_at"]
    )
    
    data = [await entity_set.to_dict() for entity_set in entity_sets]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看实体集合详情")
async def get_entity_set(
    entity_id: int = Query(..., description="实体ID"),
):
    entity_set = await entity_set_controller.get(id=entity_id)
    data = await entity_set.to_dict()
    return Success(data=data)


@router.post("/create", summary="创建实体集合")
async def create_entity_set(
    entity_in: EntitySetCreate,
):
    # 检查名称是否已存在
    existing = await entity_set_controller.get_by_name(entity_in.name)
    if existing:
        return Fail(msg=f"实体名称 '{entity_in.name}' 已存在")
    
    await entity_set_controller.create(obj_in=entity_in)
    return Success(msg="创建成功")


@router.post("/update", summary="更新实体集合")
async def update_entity_set(
    entity_in: EntitySetUpdate,
):
    # 检查名称是否与其他实体重复
    if entity_in.name:
        existing = await entity_set_controller.get_by_name(entity_in.name)
        if existing and existing.id != entity_in.id:
            return Fail(msg=f"实体名称 '{entity_in.name}' 已被其他实体使用")
    
    await entity_set_controller.update(id=entity_in.id, obj_in=entity_in)
    return Success(msg="更新成功")


@router.delete("/delete", summary="删除实体集合")
async def delete_entity_set(
    entity_id: int = Query(..., description="实体ID"),
):
    await entity_set_controller.remove(id=entity_id)
    return Success(msg="删除成功")

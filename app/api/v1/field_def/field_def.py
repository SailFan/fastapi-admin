import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.entity_set import entity_set_controller
from app.controllers.field_def import field_def_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.field_def import FieldDefCreate, FieldDefUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看字段定义列表")
async def list_field_def(
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量"),
    entity_id: int = Query(None, description="实体ID"),
    name: str = Query(None, description="字段名称（模糊查询）"),
    type: str = Query(None, description="字段类型"),
):
    search = Q()
    if entity_id:
        search &= Q(entity_id=entity_id)
    if name:
        search &= Q(name__icontains=name)
    if type:
        search &= Q(type=type)
    
    total, field_defs = await field_def_controller.list(
        page=page,
        page_size=page_size,
        search=search,
        order=["entity_id", "order"]
    )
    
    data = [await field_def.to_dict() for field_def in field_defs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看字段定义详情")
async def get_field_def(
    field_id: int = Query(..., description="字段ID"),
):
    field_def = await field_def_controller.get(id=field_id)
    data = await field_def.to_dict()
    return Success(data=data)


@router.get("/by_entity", summary="获取指定实体的所有字段定义")
async def get_fields_by_entity(
    entity_id: int = Query(..., description="实体ID"),
):
    # 检查实体是否存在
    entity = await entity_set_controller.get(id=entity_id)
    if not entity:
        return Fail(msg=f"实体ID {entity_id} 不存在")
    
    field_defs = await field_def_controller.get_by_entity_id(entity_id)
    data = [await field_def.to_dict() for field_def in field_defs]
    return Success(data=data)


@router.post("/create", summary="创建字段定义")
async def create_field_def(
    field_in: FieldDefCreate,
):
    # 检查实体是否存在
    entity = await entity_set_controller.get(id=field_in.entity_id)
    if not entity:
        return Fail(msg=f"实体ID {field_in.entity_id} 不存在")
    
    # 检查同一实体下字段名称是否已存在
    existing = await field_def_controller.get_by_name(field_in.entity_id, field_in.name)
    if existing:
        return Fail(msg=f"实体下已存在字段名称 '{field_in.name}'")
    
    await field_def_controller.create(obj_in=field_in)
    return Success(msg="创建成功")


@router.post("/update", summary="更新字段定义")
async def update_field_def(
    field_in: FieldDefUpdate,
):
    # 如果更新了实体ID，检查新实体是否存在
    if field_in.entity_id:
        entity = await entity_set_controller.get(id=field_in.entity_id)
        if not entity:
            return Fail(msg=f"实体ID {field_in.entity_id} 不存在")
    
    # 如果更新了字段名称，检查是否与同实体下其他字段重复
    if field_in.name:
        current_field = await field_def_controller.get(id=field_in.id)
        entity_id = field_in.entity_id if field_in.entity_id else current_field.entity_id
        existing = await field_def_controller.get_by_name(entity_id, field_in.name)
        if existing and existing.id != field_in.id:
            return Fail(msg=f"实体下已存在字段名称 '{field_in.name}'")
    
    await field_def_controller.update(id=field_in.id, obj_in=field_in)
    return Success(msg="更新成功")


@router.delete("/delete", summary="删除字段定义")
async def delete_field_def(
    field_id: int = Query(..., description="字段ID"),
):
    await field_def_controller.remove(id=field_id)
    return Success(msg="删除成功")


@router.delete("/delete_by_entity", summary="删除指定实体的所有字段定义")
async def delete_fields_by_entity(
    entity_id: int = Query(..., description="实体ID"),
):
    count = await field_def_controller.delete_by_entity_id(entity_id)
    return Success(msg=f"已删除 {count} 个字段定义")

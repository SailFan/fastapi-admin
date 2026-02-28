from typing import List, Optional
from uuid import UUID

from app.core.crud import CRUDBase
from app.models.field_def import FieldDef
from app.schemas.field_def import FieldDefCreate, FieldDefUpdate


class FieldDefController(CRUDBase[FieldDef, FieldDefCreate, FieldDefUpdate]):
    def __init__(self):
        super().__init__(model=FieldDef)

    async def get_by_uuid(self, uuid: UUID) -> Optional["FieldDef"]:
        """通过 UUID 获取字段定义"""
        return await self.model.filter(uuid=uuid).first()

    async def get_by_entity_id(self, entity_id: int) -> List["FieldDef"]:
        """获取指定实体的所有字段定义"""
        return await self.model.filter(entity_id=entity_id).order_by("order")

    async def get_by_name(self, entity_id: int, name: str) -> Optional["FieldDef"]:
        """通过实体ID和字段名称获取字段定义"""
        return await self.model.filter(entity_id=entity_id, name=name).first()

    async def delete_by_entity_id(self, entity_id: int) -> int:
        """删除指定实体的所有字段定义"""
        return await self.model.filter(entity_id=entity_id).delete()


field_def_controller = FieldDefController()

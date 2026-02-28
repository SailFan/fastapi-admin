from typing import Optional
from uuid import UUID

from app.core.crud import CRUDBase
from app.models.entity_set import EntitySet
from app.schemas.entity_set import EntitySetCreate, EntitySetUpdate


class EntitySetController(CRUDBase[EntitySet, EntitySetCreate, EntitySetUpdate]):
    def __init__(self):
        super().__init__(model=EntitySet)

    async def get_by_uuid(self, uuid: UUID) -> Optional["EntitySet"]:
        """通过 UUID 获取实体"""
        return await self.model.filter(uuid=uuid).first()

    async def get_by_name(self, name: str) -> Optional["EntitySet"]:
        """通过名称获取实体"""
        return await self.model.filter(name=name).first()


entity_set_controller = EntitySetController()

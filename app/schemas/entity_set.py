from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BaseEntitySet(BaseModel):
    """实体集合基础模型"""
    id: int
    uuid: UUID
    name: str
    category: Optional[str] = None
    tags: Optional[dict] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EntitySetCreate(BaseModel):
    """创建实体集合"""
    name: str = Field(..., example="User", description="实体名称")
    category: Optional[str] = Field(None, example="业务实体", description="实体类别")
    tags: Optional[dict] = Field(None, example={"type": "core", "version": "1.0"}, description="标签")
    description: Optional[str] = Field(None, example="用户实体，用于管理系统用户信息", description="业务说明")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class EntitySetUpdate(BaseModel):
    """更新实体集合"""
    id: int = Field(..., description="实体ID")
    name: Optional[str] = Field(None, example="User", description="实体名称")
    category: Optional[str] = Field(None, example="业务实体", description="实体类别")
    tags: Optional[dict] = Field(None, example={"type": "core", "version": "1.0"}, description="标签")
    description: Optional[str] = Field(None, example="用户实体，用于管理系统用户信息", description="业务说明")


class EntitySetQuery(BaseModel):
    """查询实体集合"""
    name: Optional[str] = Field(None, description="实体名称（模糊查询）")
    category: Optional[str] = Field(None, description="实体类别")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")

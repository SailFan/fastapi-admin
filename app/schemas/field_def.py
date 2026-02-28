from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BaseFieldDef(BaseModel):
    """字段定义基础模型"""
    id: int
    uuid: UUID
    entity_id: int
    name: str
    type: str
    is_required: bool = True
    default_value: Optional[str] = None
    scope: str = 'single'
    dependencies: Optional[dict] = None
    description: Optional[str] = None
    order: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class FieldDefCreate(BaseModel):
    """创建字段定义"""
    entity_id: int = Field(..., description="对应实体ID")
    name: str = Field(..., example="email", description="字段名称")
    type: str = Field(..., example="string", description="字段类型：string/int/float/date/enum/json")
    is_required: bool = Field(True, description="是否必填")
    default_value: Optional[str] = Field(None, example="user@example.com", description="默认值或占位值")
    scope: str = Field('single', example="single", description="生成模式：single/batch/optional")
    dependencies: Optional[dict] = Field(None, example={"depends_on": "user_id"}, description="字段依赖关系")
    description: Optional[str] = Field(None, example="用户邮箱地址", description="字段说明")
    order: int = Field(0, description="字段顺序")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class FieldDefUpdate(BaseModel):
    """更新字段定义"""
    id: int = Field(..., description="字段ID")
    entity_id: Optional[int] = Field(None, description="对应实体ID")
    name: Optional[str] = Field(None, example="email", description="字段名称")
    type: Optional[str] = Field(None, example="string", description="字段类型")
    is_required: Optional[bool] = Field(None, description="是否必填")
    default_value: Optional[str] = Field(None, description="默认值或占位值")
    scope: Optional[str] = Field(None, description="生成模式")
    dependencies: Optional[dict] = Field(None, description="字段依赖关系")
    description: Optional[str] = Field(None, description="字段说明")
    order: Optional[int] = Field(None, description="字段顺序")


class FieldDefQuery(BaseModel):
    """查询字段定义"""
    entity_id: Optional[int] = Field(None, description="实体ID")
    name: Optional[str] = Field(None, description="字段名称（模糊查询）")
    type: Optional[str] = Field(None, description="字段类型")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")

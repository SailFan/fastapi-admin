from tortoise import fields

from .base import BaseModel, TimestampMixin


class EntitySet(BaseModel, TimestampMixin):
    """实体集合模型"""
    
    uuid = fields.UUIDField(unique=True, pk=False, index=True, description="UUID标识")
    name = fields.CharField(max_length=100, description="实体名称", index=True)
    category = fields.CharField(max_length=50, null=True, description="实体类别", index=True)
    tags = fields.JSONField(null=True, description="可扩展标签或特征")
    description = fields.TextField(null=True, description="业务说明")

    class Meta:
        table = "entity_set"

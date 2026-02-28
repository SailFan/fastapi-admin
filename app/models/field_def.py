from tortoise import fields

from .base import BaseModel, TimestampMixin


class FieldDef(BaseModel, TimestampMixin):
    """字段定义模型"""
    
    uuid = fields.UUIDField(unique=True, pk=False, index=True, description="字段唯一标识")
    entity_id = fields.BigIntField(description="对应实体ID", index=True)
    name = fields.CharField(max_length=100, description="字段名称", index=True)
    type = fields.CharField(max_length=20, description="字段类型：string/int/float/date/enum/json", index=True)
    is_required = fields.BooleanField(default=True, description="是否必填")
    default_value = fields.TextField(null=True, description="默认值或占位值")
    scope = fields.CharField(max_length=20, default='single', description="生成模式：single/batch/optional")
    dependencies = fields.JSONField(null=True, description="字段依赖关系")
    description = fields.TextField(null=True, description="字段说明")
    order = fields.IntField(default=0, description="字段顺序", index=True)

    class Meta:
        table = "field_def"

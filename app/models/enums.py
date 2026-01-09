# app/models/enums.py
from enum import Enum, StrEnum

class EnumBase(Enum):
    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls]

    @classmethod
    def get_member_names(cls):
        return list(cls.__members__.keys())


# 替代 StrEnum：继承 (str, Enum)
class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

# 新增model需要在这里导入
from .admin import User, Role, Api, Menu, Dept, DeptClosure, AuditLog

__all__ = [
    "User", "Role", "Api", "Menu", "Dept", "DeptClosure", "AuditLog"
]

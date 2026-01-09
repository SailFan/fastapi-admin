# init_db.py
import os
import sys
from pathlib import Path
import asyncio
from tortoise import Tortoise

# 👇【核心】将项目根目录加入 Python 模块搜索路径
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

# 可选：打印当前路径，用于调试
print("Python path:", sys.path[0])
print("Looking for app.models...")

async def init():
    await Tortoise.init(
        # postgres: // admin: 123456 @ localhost:5432 / fastapi - admin
        db_url="postgres://admin:123456@localhost:5432/fastapi_admin",
        modules={"models": ["app.models"]},  # 注意：这里是字符串，不是变量
    )
    await Tortoise.generate_schemas()
    print("✅ 所有表已创建！")

if __name__ == "__main__":
    asyncio.run(init())
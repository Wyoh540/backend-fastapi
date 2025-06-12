from fastapi import APIRouter

from app.api.routes import items, users, login, file


api_router = APIRouter()

# 登录认证相关路由
api_router.include_router(login.router)
# 用户相关路由
api_router.include_router(users.router)
# 项目相关路由
api_router.include_router(items.router)
# 文件相关路由
api_router.include_router(file.router)

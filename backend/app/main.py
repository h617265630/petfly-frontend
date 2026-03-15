"""
PetFly Backend - FastAPI Application
宠物陪飞匹配平台后端
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, tasks, applications, notifications, pets

app = FastAPI(
    title="PetFly API",
    description="宠物陪飞匹配平台后端API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(pets.router, prefix="/api/pets", tags=["宠物"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务"])
app.include_router(applications.router, prefix="/api/applications", tags=["申请"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["通知"])

@app.get("/")
async def root():
    return {"message": "PetFly API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

"""
FastAPI 主程式
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(
    title="Gait Recognition API",
    description="步態識別系統 API",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite 預設端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(routes.router)


@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "Gait Recognition API",
        "version": "1.0.0",
        "docs": "/docs"
    }


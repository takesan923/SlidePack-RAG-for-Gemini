from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.v1_rag import v1_router

app = FastAPI()

# CORS設定（フロントエンド接続用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/slidepack")

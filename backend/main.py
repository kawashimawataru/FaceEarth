from fastapi import FastAPI
from routers import items, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# フロントエンドと通信するためのCORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # セキュリティ上は特定のドメインに限定するのがベター
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを追加
app.include_router(items.router, prefix="/items")
app.include_router(users.router, prefix="/users")

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI + React!"}

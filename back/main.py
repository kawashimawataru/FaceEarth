# こちらは 
# http://127.0.0.1:8000/

# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import io
from similarity import find_most_similar_image

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"Hello": "World!"}

@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    api_key: str = Form(...),
    location: str = Form(...)
):
    # 画像データをバイナリとして読み込み
    content = await image.read()
    # BytesIO 経由で PIL で読み込める形式に変換
    image_file = io.BytesIO(content)

    # 画像の類似度を計算（※find_most_similar_image 内で PIL.Image.open() を使うように実装を調整する必要あり）
    similarity_result = find_most_similar_image(image_file, api_key, location)

    return {
        "similarity": similarity_result["similarity"],
        "latitude": similarity_result["latitude"],
        "longitude": similarity_result["longitude"]
    }

# こちらは 
# http://127.0.0.1:8000/

# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import io
from modules.similarity import find_most_similar_image, draw_matches
from fastapi.responses import StreamingResponse  # ← これを追加

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

    # 固定の参照画像を読み込む例
    with open("image_test/森和也_earth.jpg", "rb") as f:
        reference_image = io.BytesIO(f.read())

    # 画像の類似度を計算（※find_most_similar_image 内で PIL.Image.open() を使うように実装を調整する必要あり）
    similarity_result = find_most_similar_image(image_file, reference_image)

    return {
        "similarity": similarity_result["similarity"],
        "latitude": similarity_result["latitude"],
        "longitude": similarity_result["longitude"]
    }

@app.post("/matched_image")
async def matched_image_endpoint(image: UploadFile = File(...)):
    """
    1. アップロードされた画像を受け取る
    2. 画像の比較 + 図示（マッチングなど）を行う
    3. 処理後の画像を PNG にエンコードして返す
    """

    # 1. ファイルを読み込み
    # 画像データをバイナリとして読み込み
    content = await image.read()
    # BytesIO 経由で PIL で読み込める形式に変換
    image_file = io.BytesIO(content)

    # 固定の参照画像を読み込む例
    with open("image_test/森和也_earth.jpg", "rb") as f:
        reference_image = io.BytesIO(f.read())

    # 2. 画像の比較 + 図示
    matched_image = draw_matches(image_file, reference_image)

    # 3. PNG形式にエンコードして StreamingResponse で返却

    return StreamingResponse(io.BytesIO(matched_image), media_type="image/png")
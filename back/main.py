# こちらは 
# http://127.0.0.1:8000/

# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import io
import random
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

# Mount static directory to serve images
app.mount("/images", StaticFiles(directory="image_test"), name="images")

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
    image_file = io.BytesIO(content)

    # 固定の参照画像を読み込む (1つ目)
    # 実運用ではデータベースから検索する
    with open("image_test/森和也_earth.jpg", "rb") as f:
        reference_image_bytes = f.read()
        reference_image = io.BytesIO(reference_image_bytes)

    # 1つ目の候補（実際に計算）
    similarity_result = find_most_similar_image(image_file, reference_image)
    
    # 候補リストを作成 (3つ)
    candidates = [
        {
            "id": 1,
            "image_url": "http://127.0.0.1:8000/images/森和也_earth.jpg",
            "similarity": similarity_result["similarity"],
            "latitude": similarity_result["latitude"],
            "longitude": similarity_result["longitude"],
            "place_name": "Izu Oshima",
            "country": "JAPAN",
            "city": "Tokyo",
            "description": "A volcanic island where the earth breathes. Your resilience resonates with the enduring strength of the magma beneath."
        },
        {
            "id": 2,
            "image_url": "http://127.0.0.1:8000/images/test.png", # 仮の画像
            "similarity": random.uniform(70.0, 85.0),
            "latitude": 40.7128,
            "longitude": -74.0060,
            "place_name": "Manhattan",
            "country": "USA",
            "city": "New York",
            "description": "The city that never sleeps. Your ambition mirrors the towering skyscrapers reaching for the infinite sky."
        },
        {
            "id": 3,
            "image_url": "http://127.0.0.1:8000/images/森和也_earth.jpg", # 画像がないので使い回し
            "similarity": random.uniform(60.0, 75.0),
            "latitude": -33.8688,
            "longitude": 151.2093,
            "place_name": "Sydney Opera House",
            "country": "AUSTRALIA",
            "city": "Sydney",
            "description": "A harbor of dreams. Your creativity flows like the waves embracing the iconic sails of the opera house."
        }
    ]

    # 類似度順にソート
    candidates.sort(key=lambda x: x["similarity"], reverse=True)

    return candidates
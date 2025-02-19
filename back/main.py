# こちらは 
# http://127.0.0.1:8000/

# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi import Body
import json
import io
from modules.similarity import find_most_similar_image, draw_matches
from modules.from_google import find_best_match_origin
from modules.question import get_random_questions
from modules.chatbot_call import call_map_generate

from fastapi.responses import StreamingResponse  # ← これを追加
from PIL import Image

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
    with open("modules/best_match_enhanced.jpg", "rb") as f:
        reference_image = io.BytesIO(f.read())

    # 2. 画像の比較 + 図示
    matched_image = draw_matches(image_file, reference_image)

    # 3. PNG形式にエンコードして StreamingResponse で返却

    return StreamingResponse(io.BytesIO(matched_image), media_type="image/png")

@app.post("/google_matched_image")
async def matched_image_endpoint(image: UploadFile = File(...)):
    """
    1. アップロードされた画像を受け取る
    2. グーグルマップ上で似ている画像を検索
    3. 処理後の画像を PNG にエンコードして返す
    """

    # 1. ファイルを読み込み
    # 画像データをバイナリとして読み込み
    content = await image.read()
    image_file = io.BytesIO(content)
    image_pil = Image.open(image_file).convert("RGB")

    # 2. 画像の比較 + 図示

    # 初期探索座標（例: 東京駅付近 35.6895, 139.6917）
    init_lat, init_lon = 35.6895, 139.6917

    matched_image = find_best_match_origin(image_pil, init_lat, init_lon)

    # 3. PNG形式にエンコードして StreamingResponse で返却
    matched_image_buffer = io.BytesIO()
    matched_image.save(matched_image_buffer, format="PNG")
    matched_image_buffer.seek(0)
    return StreamingResponse(matched_image_buffer, media_type="image/png")

@app.get("/get_random_questions")
async def random_questions_endpoint():
    random_questions = get_random_questions()
    return JSONResponse(content=random_questions)

@app.post("/map_generate")
async def map_generate(json_data: list = Body(...)):
    """
    1. ユーザーの回答データ（リスト形式）を受け取る
    2. マップ生成のためのプロンプトを作成
    3. マップ生成エンドポイントにリクエストを送信
    4. レスポンスを返す
    """
    data_str = json.dumps(json_data, ensure_ascii=False)
    ansewer = call_map_generate(data_str)
#     ansewer = """

# {
#   "candidates": [
#     {
#       "avgLogprobs": -0.03646521036476179,
#       "content": {
#         "parts": [
#           {
#             "text": "```json\n{\n  \"user_responses\": [\n    {\n      \"question_id\": \"Q1-1\",\n      \"question_text\": \"暖かい場所と寒い場所、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"暖かい\", \"寒い\"],\n      \"user_choice\": \"暖かい\",\n      \"scoring\": { \"warm\": 2, \"tropical\": 2, \"cold\": 0 }\n    },\n    {\n      \"question_id\": \"Q2-1\",\n      \"question_text\": \"自然豊かな場所と都会的な場所、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"自然豊かな場所\", \"都会的な場所\"],\n      \"user_choice\": \"都会的な場所\",\n      \"scoring\": { \"nature\": 0, \"city\": 2 }\n    },\n    {\n      \"question_id\": \"Q3-1\",\n      \"question_text\": \"アクティブな旅行とゆったりとした旅行、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"アクティブな旅行\", \"ゆったりとした旅行\"],\n      \"user_choice\": \"ゆったりとした旅行\",\n      \"scoring\": { \"active\": 0, \"relax\": 2 }\n    },\n    {\n      \"question_id\": \"Q4-1\",\n      \"question_text\": \"歴史的な場所と近代的な場所、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"歴史的な場所\", \"近代的な場所\"],\n      \"user_choice\": \"近代的な場所\",\n      \"scoring\": { \"historical\": 0, \"modern\": 2 }\n    }\n  ]\n}\n```\n\n```python\nuser_responses = {\n  \"user_responses\": [\n    {\n      \"question_id\": \"Q1-1\",\n      \"question_text\": \"暖かい場所と寒い場所、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"暖かい\", \"寒い\"],\n      \"user_choice\": \"暖かい\",\n      \"scoring\": { \"warm\": 2, \"tropical\": 2, \"cold\": 0 }\n    },\n    {\n      \"question_id\": \"Q2-1\",\n      \"question_text\": \"自然豊かな場所と都会的な場所、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"自然豊かな場所\", \"都会的な場所\"],\n      \"user_choice\": \"都会的な場所\",\n      \"scoring\": { \"nature\": 0, \"city\": 2 }\n    },\n    {\n      \"question_id\": \"Q3-1\",\n      \"question_text\": \"アクティブな旅行とゆったりとした旅行、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"アクティブな旅行\", \"ゆったりとした旅行\"],\n      \"user_choice\": \"ゆったりとした旅行\",\n      \"scoring\": { \"active\": 0, \"relax\": 2 }\n    },\n    {\n      \"question_id\": \"Q4-1\",\n      \"question_text\": \"歴史的な場所と近代的な場所、どちらが好き？\",\n      \"type\": \"YesNo\",\n      \"options\": [\"歴史的な場所\", \"近代的な場所\"],\n      \"user_choice\": \"近代的な場所\",\n      \"scoring\": { \"historical\": 0, \"modern\": 2 }\n    }\n  ]\n}\n\n\nlocations = [\n    [\"シンガポール:シンガポール島:1.3521,103.8198\"],\n    [\"ドバイ:ドバイ:25.2048,55.2708\"],\n    [\"香港:香港島:22.2855,114.1577\"]\n]\n\ndescriptions = [\n    \"シンガポール：熱帯の息吹と未来都市の調和。洗練された街並みを散策し、多様な文化に触れ、穏やかな時間を過ごせるでしょう。きらめく夜景は、忘れられない思い出となるでしょう。\",\n    \"ドバイ：砂漠のオアシスに建つ摩天楼。壮大なスケールと近未来的なデザインに圧倒され、贅沢なひとときを満喫できるでしょう。砂漠の静寂と都会の喧騒が織りなす、独特の雰囲気に酔いしれてください。\",\n    \"香港：東洋の真珠と呼ばれる香港。活気あふれる街並みと、伝統と近代が融合した独特の文化があなたを魅了します。維多リア湾の美しい景色を眺めながら、ゆったりとした時間をお過ごしください。\"\n]\n\nprint(locations)\nprint(descriptions)\n```\n"
#           }
#         ],
#         "role": "model"
#       },
#       "finishReason": "STOP"
#     }
#   ],
#   "modelVersion": "gemini-1.5-flash",
#   "usageMetadata": {
#     "candidatesTokenCount": 1058,
#     "candidatesTokensDetails": [
#       {
#         "modality": "TEXT",
#         "tokenCount": 1058
#       }
#     ],
#     "promptTokenCount": 776,
#     "promptTokensDetails": [
#       {
#         "modality": "TEXT",
#         "tokenCount": 776
#       }
#     ],
#     "totalTokenCount": 1834
#   }
# }

#     """
#     print(ansewer)
    return ansewer
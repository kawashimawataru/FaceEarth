import functions_framework
import requests
import os
import re
import time

# Google API キー
GEMINI_API_KEY = "AIzaSyBhLqOgjqNh7pW1Qyp4VNmAj1ewi1O0OR4"
GOOGLE_SEARCH_API_KEY = "AIzaSyBnwwiC_no_dMqTjNpVscVSenCuKzoP0dM"
CX = "a5b5189ba91d0415f"

def call_gemini_api(payload):
    """Gemini APIを呼び出し、503エラーの場合はリトライする"""
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    max_retries = 5
    wait_time = 5

    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 503:
            print(f"Gemini API オーバーロード: {attempt + 1}/{max_retries} 回目のリトライ")
            time.sleep(wait_time)
            wait_time *= 2  

        else:
            break 

    return {"error": "Gemini API is unavailable. Please try again later."}

def clean_search_query(query):
    """検索クエリから不要な記号や装飾を削除"""
    query = re.sub(r"[*\n]", "", query)  # 不要な * や 改行を削除
    query = query.strip()  # 前後の余計なスペースを削除
    return query

@functions_framework.http
def root_help2(request):
    """Cloud Functions で 2回 LLM を使い、検索を活用して正確な回答を生成"""
    
    # リクエストの JSON を取得
    request_json = request.get_json(silent=True)
    conversation_log = request_json.get("conversation", "")

    # **LLM2: 最終回答を生成**
    system_instruction = f"""
    あなたは「候補地選出AI」です。  
    ユーザーの回答データを解析し、最適な土地をリストアップしてください。  

    ---

    <目的>
    - ユーザーの回答を数値化し、最適な土地を提案する  
    - 候補地ごとにスコアを計算し、適合度の高いものをリストアップする  
    - 各候補地の特徴を説明し、ユーザーに納得感を持たせる

    <入力データフォーマット:json>
    ```{{
        "user_responses": [
            {{
            "question_id": "Q1-1",
            "question_text": "暖かい場所と寒い場所、どちらが好き？",
            "type": "YesNo",
            "options": ["暖かい", "寒い"],
            "user_choice": "暖かい",
            "scoring": {{ "warm": 2, "tropical": 2 }}
            }},
            {{
            "question_id": "Q1-2",
            "question_text": "海が好きですか？",
            "type": "YesNo",
            "options": ["はい", "いいえ"],
            "user_choice": "はい",
            "scoring": {{ "coastal": 3 }}
            }},
            {{
            "question_id": "Q2-1",
            "question_text": "どんな環境に惹かれますか？",
            "type": "choice",
            "options": ["都会のネオン", "静かな森", "歴史ある街並み", "広大な砂漠"],
            "user_choice": "都会のネオン",
            "scoring": {{ "urban": 6 }}
            }},
            {{
            "question_id": "Q3-1",
            "question_text": "あなたの性格を動物に例えるなら？",
            "type": "choice2",
            "options": ["🦅 鷹", "🐢 亀", "🦊 狐", "🐬 イルカ"],
            "user_choice": "🦊 狐",
            "scoring": {{ "mysterious": 3, "forest": 2 }}
            }},
            {{
            "question_id": "Q4-1",
            "question_text": "次の4つの風景の中で、一番好きなものを選んでください。",
            "type": "image",
            "options": [
                {{ "image": "ocean.jpg", "label": "海" }},
                {{ "image": "mountain.jpg", "label": "山" }},
                {{ "image": "city.jpg", "label": "都会" }},
                {{ "image": "desert.jpg", "label": "砂漠" }}
            ],
            "user_choice": "city.jpg",
            "scoring": {{ "urban": 3 }}
            }}
        ],
        "total_scoring": {{
            "warm": 2,
            "tropical": 2,
            "coastal": 3,
            "urban": 9,
            "mysterious": 3,
            "forest": 2
        }}
        }}```
    """

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_instruction}]},
            {"role": "user", "parts": [{"text": f"入力\n{conversation_log}\n\nこれに基づいて旅行プランを作成してください。"}]}
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }

    response = call_gemini_api(payload)

    return response if response else {"error": "Failed to generate response."}

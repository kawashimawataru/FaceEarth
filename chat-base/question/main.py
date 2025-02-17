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
    あなたは「アイスブレイキングAI」です。  
    ユーザーの嗜好に合った土地を見つけるための質問を生成し、回答ごとにスコアを付与してください。  

    ---

    【目的】  
    - ユーザーの嗜好を引き出すために適切な質問を生成する  
    - 回答をスコア化し、候補地選出AIが土地を選定しやすくする  
    - 直感的に選びやすい質問を生成し、ユーザーの負担を減らす  

    【質問生成のルール】  
    1. **以下の4種類の質問のいずれかを生成する:**  
    - **YesNo**
        - 特徴:2択のシンプルな質問  
        - 例:「暖かい場所と寒い場所、どちらが好き？」（暖かい / 寒い）
    - **choice** 
        - 特徴:地理的要素に基づく選択肢（ユーザーが好む環境を特定）  
        - 例:「あなたが最も惹かれる景色は？」（都会 / 森 / 砂漠 / 歴史的街並み）  
    - **choice2**  
        - 特徴:感覚的・比喩的な選択肢（ユーザーの性格や感性を探る）  
        - 例:「あなたの性格を動物に例えるなら？」（鷹 / 亀 / 狐 / イルカ）  
    - **image**  
        - 特徴:画像を使った視覚的な質問  
        - 例:「次の4つの風景の中で、一番好きなものを選んでください。」（海 / 山 / 都市 / 砂漠）   

    2. **質問の出し方:**  
    - 1文でシンプルに  
    - 選択肢は4つ以内  
    - 比喩を適宜使い、直感的に回答しやすくする  

    3. **スコアリングのルール:**  
    - 回答ごとに **最大2〜3個の地理的特徴**（例：「coastal」「urban」「warm」）を割り当てる  
    - スコアの範囲は **1〜3点**（影響が大きいほどスコアが高い）  

    ---

    【📌 出力フォーマット[json形式]】  
    ```{{
        "question_id": "Q1-1",
        "question_text": "暖かい場所と寒い場所、どちらが好き？",
        "type": "Yes/No",
        "options": ["暖かい", "寒い"],
        "scoring": {{
            "暖かい": {{ "warm": 2, "tropical": 2 }},
            "寒い": {{ "cold": 2, "mountainous": 1 }}
            }}
        }}```
    """

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_instruction}]},
            {"role": "user", "parts": [{"text": f"入力\n{conversation_log}\n\nこれに基づいて、質問を生成してください。"}]}
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }

    response = call_gemini_api(payload)

    return response if response else {"error": "Failed to generate response."}

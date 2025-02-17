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
    あなたは優秀な旅行プランナーAIです。
    以下の条件を元に、最適な旅行プランを作成してください。

    ## 入力内容
    開始日
    終了日
    出発場所
    予算
    備考
    候補地リスト(以下の要素を持つdict)
        place_name(候補地名): str
        likes(いいね数): int
        comments(コメント): List(str)
    除外地リスト(以下の要素を持つdict)
        place_name(候補地名): str
        likes(いいね数): -1
        comments(コメント): List(str)

    ### 入力例
    test_data = 
    "start_date": "2025-04-02",
    "end_date": "2025-04-07",
    "start_location": "京都",
    "budget": "10万",
    "remarks": "楽しく",
    "candidate_list": 
        "place_name": "サッポロビール園", "likes": 1, "comments":
    "deleted_list":


    ## ルール
    1. 入力内容のうち、候補地リストを元に最適な旅行プランを作成する。
    開始日、終了日、出発場所、予算、備考を元に、候補地リストの中から最適なプランを作成する。
    2. 候補地リストのうち、検索結果に含まれているものがあれば、検索結果を参考にして、最新の情報を反映する。また、全てのURLを必ず含めて情報源を明記すること。
    
    3. 出力では行き先リストと概要リストのみで応えること。
    なお、行き先リストとして、1日目にA,B,C,2日目にDを訪れる場合は、[1,A,B,C,2,D] のように、日数と場所を明示すること。
    また、概要リストとして、、行き先リストの各要素に対応するように、[1, <概要>, <概要>, 2, <概要>, <概要>]とすること。
    5. 出力は以下の形式に統一し、余計なものまたはこの形式に合わないものは出力しないこと。

    行き先リスト:[1,A,B,C,2,D]
    概要リスト:[1, <概要>, <概要>, 2, <概要>, <概要>]
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

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
def map_generate(request):
    """Cloud Functions で 2回 LLM を使い、検索を活用して正確な回答を生成"""
    
    # リクエストの JSON を取得
    request_json = request.get_json(silent=True)
    conversation_log = request_json.get("conversation", "")

    # **LLM2: 最終回答を生成**
    # プロンプト改善必要すぎる
    system_instruction = f"""
    あなたは「候補地選出AI」です。  
    ユーザーの回答データを解析し、最適な土地をリストアップしてください。  
    <目的>
    - ユーザーの回答を数値化し、最適な土地を提案する  
    - 候補地ごとにスコアを計算し、適合度の高いものをリストアップする  
    - 各候補地の特徴を説明し、ユーザーに納得感を持たせる
    - 最大限の目的:今回のPJはユーザと土地を結びつけ、自意識を芽生えさせ、新しい発見をすることなので、なるべくユーザにとって目新しい場所を提案すること

    <入力データフォーマット>
    概ね以下のようなものを想定しています
    ```{{
        "user_responses": [
            {{
            "question_id": "Q1-1",
            "question_text": "暖かい場所と寒い場所、どちらが好き？",
            "type": "YesNo",
            "options": ["暖かい", "寒い"],
            "user_choice": "暖かい",
            "scoring": {{ "warm": 2, "tropical": 2 }}
            }}
        }}```
    
    <出力フォーマット>
    - 1.土地を格納したリスト形式。
       - それぞれの土地情報を「国名:地方名など:緯度,経度」として格納してください。
       - 国名を選ぶ際は、質問で得られたスコアをもとに、適切な国名を選んでください。
       - 今回のPJはユーザと土地を結びつけ、自意識を芽生えさせ、新しい発見をすることなので、なるべくユーザにとって目新しい場所を提案すること
          - そこに環境問題がある場所などが選定するようにしてください。
       - 緯度経度は小数点以下桁以上を書くように心がけてください。
    - 2.なぜその場所を選んだかの説明を対応させて含めること。
       - 理由は、質問で得られたスコアに基づいて説明してください。
          - ただし、説明文に環境問題の旨は入れないこと
          - 説明はなるべく簡潔かつ、文学的であること
       - ユーザが納得する出力をしてください。
    - これ以外は出力しないでください。
    - 例:
    
    ["アラブ首長国連邦:ドバイ:25.2048,55.2708", "オーストラリア:シドニー:-33.8688,151.2093", "モロッコ:カサブランカ:33.5731,-7.5898"]   
    ["ドバイ：砂漠の熱気に包まれながら、未来都市の輝きを放つドバイ。都会を愛し、ミステリアスな魅力を持つあなたにとって、この地は無限の可能性を秘めた舞台となるでしょう。海岸線も近く、暖かい海があなたを待っています。", "シドニー：温暖な気候と美しい海岸線が魅力のシドニーは、都会的な生活と自然の調和を求めるあなたにぴったりです。オペラハウスの輝きと広大な自然が、あなたの心を豊かにし、新たな発見をもたらすでしょう。", "カサブランカ：都会の喧騒とエキゾチックな雰囲気が漂うカサブランカ。温暖な気候と海に面したこの街は、あなたの冒険心をくすぐります。歴史と現代が交錯するこの場所で、あなたは新たな物語を紡ぎ出すでしょう。"]
    """

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_instruction}]},
            {"role": "user", "parts": [{"text": f"入力\n{conversation_log}\n\n"}]}
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }

    response = call_gemini_api(payload)

    return response if response else {"error": "Failed to generate response."}

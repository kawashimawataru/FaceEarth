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

def extract_search_topics(conversation_log):
    """LLM1: ユーザーの入力から検索すべき内容を3つ選ぶ"""
    system_instruction = """
    あなたは優秀な検索エンジン補助AIです。
    ユーザーの入力内容から、検索すべき **最適なトピックを4つ** 選んでください。

    ## ルール
    1. その土地の重要な情報を調べる。
    2. 歴史・環境問題は必ず含め、そのほか実用的な情報を含める
    3. 曖昧なワードは避け、具体的なワードを選ぶ。仮にない場合は、おすすめのものを考えて選ぶ
    4. * や ** などの装飾を含めないこと
    """

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_instruction}]},
            {"role": "user", "parts": [{"text": f"ユーザー入力:\n{conversation_log}\n\nこの内容から、検索すべきトピックを3つ出力してください。"}]}
        ],
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 128
        }
    }

    response = call_gemini_api(payload)

    if "candidates" in response:
        topics = response["candidates"][0]["content"]["parts"][0]["text"].split("\n")[:3]  # 3つ取得
        cleaned_topics = [clean_search_query(topic) for topic in topics]  # クエリをクリーニング
        return cleaned_topics
    else:
        return ["環境問題", "SDGs", "政治経済"]  # デフォルト値

def google_search(query, num_results=2):
    """Google検索APIを利用して、参考となるサイトを取得"""
    query = clean_search_query(query)  # クエリの不要な記号を削除

    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": CX,
        "num": num_results,
    }

    response = requests.get(url, params=params)
    response_json = response.json()

    # **エラーハンドリング**
    if "items" not in response_json:
        print(f"❌ 検索結果が見つかりません: {response_json}")
        return []

    results = response_json["items"]

    # **タイトルとURLを取得**
    search_data = []
    for item in results:
        title = item.get("title", "タイトルなし")
        link = item.get("link", "URLなし")
        search_data.append({"title": title, "link": link})

    return search_data

@functions_framework.http
def root_help2(request):
    """Cloud Functions で 2回 LLM を使い、検索を活用して正確な回答を生成"""
    
    # リクエストの JSON を取得
    request_json = request.get_json(silent=True)
    conversation_log = request_json.get("conversation", "")

    # **LLM1: 検索すべきトピックを抽出**
    search_topics = extract_search_topics(conversation_log)
    print(f"検索トピック（修正後）: {search_topics}")  # デバッグ用

    # **Google検索でトピックごとに参考サイトを取得**
    search_results = {}
    for topic in search_topics:
        search_results[topic] = google_search(topic)

    # **検索結果を整形**
    search_info = ""
    search_info_urls = []
    for topic, results in search_results.items():
        search_info += f"\n**{topic}**\n"
        for item in results:
            search_info += f"- [{item['title']}]({item['link']})\n"
            search_info_urls.append(item["link"])

    # **LLM2: 最終回答を生成**
    system_instruction = f"""
    あなたは「候補地説明AI」です。
    与えられる画像はユーザの入力画像と、類似した土地の画像の二つです。
    ユーザーの回答データと検索結果を解析し、土地に対するメッセージを生成してください。  

    ---

    <目的>
    - 各候補地の特徴を説明し、ユーザーに納得感を持たせる

    <生成ルール>
    - 入力データに対して、以下のような文章で生成すること
    - 土地に関して、特徴や魅力を説明する文章を生成する。
    - 最後に、


    <入力データフォーマット1:image>
    image1:ユーザの入力画像
    image2:類似した土地の画像

    <入力データフォーマット2:検索結果>
    ## 検索結果
    {search_info}

    ## 参考情報URL
    {', '.join(search_info_urls)}

    <入力データフォーマット3:ユーザ回答>

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

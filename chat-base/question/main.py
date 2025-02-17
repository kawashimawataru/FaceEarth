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
    1. 旅行に関連する内容を優先
    2. 地名・グルメ・アクティビティなど、実用的な情報を含める
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
        return ["東北 旅行プラン", "東北 グルメ", "東北 宿泊施設"]  # デフォルト値

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
    ## 検索結果
    {search_info}

    ## 参考情報URL
    {', '.join(search_info_urls)}
    
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

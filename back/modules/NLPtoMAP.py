import mediapipe as mp  # ※将来的な利用を見越して残しています
import requests
import random
import math
import json

############################
# ユーザーの入力のために、質問をする関数
# ※Geminiが生成する関数としても利用可能
############################
def ask_user_input():
    """
    ユーザーの質問を生成する関数。
    
    """
    return input(prompt)

############################
# Cloud Function 経由でGemini AIに問い合わせる関数
############################
def call_gemini_travel_helper(conversation, ai_prompt):
    """
    Google CloudのCloud Functionを利用してGemini AIに問い合わせる関数
    
    Args:
        conversation (list): 過去の会話履歴など（例: [{"role": "user", "content": "～"}]）
        ai_prompt (str): AIへのプロンプト
    
    Returns:
        str: Geminiからの返答テキスト。応答が得られなかった場合は None
    """
    endpoint = "https://us-central1-goukan2house.cloudfunctions.net/travel_helper"
    headers = {"Content-Type": "application/json"}
    payload = {"conversation": conversation, "ai_prompt": ai_prompt}
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data_json = response.json()
        # ※ Cloud Function側のレスポンス形式に合わせてパースする
        candidate_text = data_json["candidates"][0]["content"]["parts"][0]["text"]
        reply_text = candidate_text.strip()
        return reply_text
    except requests.exceptions.RequestException as e:
        print(f"Cloud Functionへのリクエストでエラーが発生しました: {e}")
        return None

############################
# ユーザーの入力に基づいて、候補地を取得するGemini版の関数
############################
def generate_candidates_from_input_gemini(user_input, gemini_api_key=None):
    """
    Gemini AI（Google CloudのCloud Function経由）を利用して候補地を取得する関数
    
    Args:
        user_input (str): ユーザーが入力した場所やキーワード
        gemini_api_key (str): 必要に応じて利用するAPIキー（現状はCloud Function側で管理）
    
    Returns:
        list of dict: 各候補は {"name": <候補地名>, "coordinates": [<緯度>, <経度>]} の形式
    """
    # Cloud Functionに渡す会話履歴とプロンプトを作成
    conversation = [{"role": "user", "content": user_input}]
    ai_prompt = (
        f"ユーザーが入力した『{user_input}』に基づいて、複数の候補地を名前と仮の座標（例としてランダムな数値）を含めたJSONを生成してください。"
        " 出力は必ず以下の形式で返してください。\n"
        '{\n'
        '  "candidates": [\n'
        '    {"name": "候補地1", "coordinates": [35.6895, 139.6917]},\n'
        '    {"name": "候補地2", "coordinates": [34.6937, 135.5023]},\n'
        '    ...\n'
        '  ]\n'
        '}\n'
    )
    
    reply_text = call_gemini_travel_helper(conversation, ai_prompt)
    if reply_text is None:
        print("Gemini AIから応答が得られなかったため、ダミーの候補を返します。")
        return _dummy_candidates(user_input)
    
    try:
        result = json.loads(reply_text)
        candidates = result.get("candidates", [])
        return candidates
    except json.JSONDecodeError:
        print("Geminiからの応答がJSONとして解釈できませんでした。ダミーの候補を返します。")
        return _dummy_candidates(user_input)

def _dummy_candidates(user_input):
    """Cloud Functionエラー時に返すダミー候補"""
    candidates = []
    for i in range(3):
        candidate = {
            "name": f"{user_input}_候補{i+1}",
            "coordinates": [
                round(random.uniform(-90, 90), 6),
                round(random.uniform(-180, 180), 6)
            ]
        }
        candidates.append(candidate)
    return candidates

############################
# Google Maps Geocoding APIを利用して、候補地名称から座標を取得する関数
############################
def get_coordinates_from_place_name(place_name, google_maps_api_key):
    """
    Google Maps Geocoding APIを利用して、候補地名称から座標を取得する関数
    
    Args:
        place_name (str): 例) "東京駅"
        google_maps_api_key (str): Google Maps Geocoding APIキー
    
    Returns:
        tuple: (緯度, 経度) のタプル。失敗時は None
    """
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place_name, "key": google_maps_api_key}
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "OK":
            results = data.get("results", [])
            if results:
                location = results[0]["geometry"]["location"]
                return (location["lat"], location["lng"])
            else:
                print(f"'{place_name}' に対する検索結果が見つかりませんでした。")
                return None
        else:
            print(f"Geocoding APIでエラーが発生しました: {data.get('status')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Google Maps Geocoding APIへのリクエストでエラーが発生しました: {e}")
        return None

############################
# Google Custom Search API等を利用して、座標に対応する場所の詳細情報を取得する関数
############################
def get_location_description(coordinates, google_search_api_key, google_search_cx):
    """
    Google検索APIを利用して、座標に対応する場所の詳細情報を取得する関数
    
    Args:
        coordinates (tuple): (緯度, 経度)
        google_search_api_key (str): GoogleのCustom Search APIキー
        google_search_cx (str): 検索エンジンID (Custom Search JSON API)
    
    Returns:
        str: 検索結果などから生成した説明文（ダミー可）
    """
    if not coordinates:
        return "座標が指定されていないため、説明を生成できませんでした。"
    
    lat, lng = coordinates
    query = f"{lat},{lng} 周辺 観光 地域情報"
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"key": google_search_api_key, "cx": google_search_cx, "q": query}
    
    try:
        # ※実際の検索結果を利用する場合は以下のコメントを外して実装してください
        # response = requests.get(endpoint, params=params)
        # response.raise_for_status()
        # data = response.json()
        # ここで data から必要な情報を抽出して説明文を生成する
        
        # ---- ダミー実装 ----
        description = (
            f"座標 {coordinates} は、自然豊かで環境に優しい地域です。"
            " 周辺には観光スポットや緑地も多く、住環境としても魅力的です。"
        )
        return description
    except requests.exceptions.RequestException as e:
        print(f"Google検索APIへのリクエストでエラーが発生しました: {e}")
        return "検索に失敗しました。"

############################
# Google Custom Search API等を利用して、クエリに対する検索結果を返す関数
############################
def search_results(query, google_search_api_key, google_search_cx):
    """
    Google Custom Search APIなどを利用して、クエリに対する検索結果を返す関数
    
    Args:
        query (str): 検索キーワード
        google_search_api_key (str): GoogleのCustom Search APIキー
        google_search_cx (str): 検索エンジンID (Custom Search JSON API)
    
    Returns:
        list: 検索結果のタイトルなどを要素としたリスト（ダミー可）
    """
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"key": google_search_api_key, "cx": google_search_cx, "q": query}
    
    try:
        # ※実際の検索結果を利用する場合は以下のコメントを外してください
        # response = requests.get(endpoint, params=params)
        # response.raise_for_status()
        # data = response.json()
        # results = [item["title"] for item in data.get("items", [])]
        
        # ---- ダミー実装 ----
        results = [
            f"{query}に関する記事 1",
            f"{query}に関する記事 2",
            f"{query}に関する記事 3"
        ]
        return results
    except requests.exceptions.RequestException as e:
        print(f"検索APIへのリクエストでエラーが発生しました: {e}")
        return []


############################
# メイン処理（テスト用）
############################
# if __name__ == "__main__":
#     # --- 各APIキーを設定してください ---
#     # ※ gemini_api_key は Cloud Function側で管理する場合は不要（又はダミー値）
#     gemini_api_key = "YOUR_GEMINI_API_KEY"
#     google_maps_api_key = "YOUR_GOOGLE_MAPS_API_KEY"
#     google_search_api_key = "YOUR_GOOGLE_SEARCH_API_KEY"
#     google_search_cx = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

#     # 1. Gemini AI を利用して候補地を取得
#     user_query = ask_user_input("候補地を探したい場所を入力してください: ")
#     candidates = generate_candidates_from_input_gemini(user_query, gemini_api_key)
#     print("候補地:")
#     for candidate in candidates:
#         print(candidate)
    
#     # 2. ユーザー指定の場所から座標を取得（Google Maps Geocoding API利用）
#     place_name = ask_user_input("詳細情報を求める候補地の名称を入力してください: ")
#     coordinates = get_coordinates_from_place_name(place_name, google_maps_api_key)
#     print(f"{place_name} の座標: {coordinates}")
    
#     # 3. 座標に基づいた場所の説明を取得（Google検索API利用）
#     description = get_location_description(coordinates, google_search_api_key, google_search_cx)
#     print("場所の説明:")
#     print(description)
    
#     # 4. 検索クエリを入力して、関連する検索結果を取得
#     search_query = ask_user_input("検索クエリを入力してください: ")
#     results = search_results(search_query, google_search_api_key, google_search_cx)
#     print("検索結果:")
#     for result in results:
#         print(result)

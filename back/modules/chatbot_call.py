import requests
import json

# エンドポイントURLは変数として定義
MAP_GENERATE_ENDPOINT = "https://us-central1-goukan2house.cloudfunctions.net/map_generate"

def call_map_generate(prompt: str):
    """
    promptの内容を含むJSONデータをPOSTし、結果のJSONを返す関数。
    """
    payload = {
        "prompt": prompt
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(MAP_GENERATE_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# テスト実行例
if __name__ == '__main__':
    sample_prompt = "あなたのプロンプト内容をここに記載"
    result = call_map_generate(sample_prompt)
    print(json.dumps(result, indent=2, ensure_ascii=False))
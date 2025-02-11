from PIL import Image
import numpy as np
import requests
from io import BytesIO
import io



# 多分ここには書かない、別のファイルに書こう

# def fetch_images_from_google_maps(api_key, location, radius=1000, max_results=100):
#     # Google Maps APIを使用して画像を取得する処理を実装
#     # ここではダミーの画像URLを返す
#     return ["http://example.com/image1.jpg", "http://example.com/image2.jpg"] * (max_results // 2)

def preprocess_image(image_file):
    # image_file はファイルオブジェクトであることを想定
    image = Image.open(image_file)
    image = image.resize((256, 256))  # リサイズ
    return np.array(image)

def calculate_image_similarity_percentage(image1, image2):
    if image1.shape != image2.shape:
        raise ValueError("比較する画像のサイズ(次元)が異なります。")
    diff = np.abs(image1.astype(np.float32) - image2.astype(np.float32))
    diff_sum = np.sum(diff)
    if len(image1.shape) == 3:
        channels = image1.shape[2]
        num_pixels = image1.shape[0] * image1.shape[1]
    else:
        channels = 1
        num_pixels = image1.shape[0] * image1.shape[1]
    max_diff = 255.0 * channels * num_pixels
    similarity = (1.0 - diff_sum / max_diff) * 100.0
    similarity = max(0.0, min(100.0, similarity))
    return similarity

def find_most_similar_image(target_image_file, api_key, location):
    target_image = preprocess_image(target_image_file)
    
    # 固定の参照画像を読み込む例
    with open("image_test/test.png", "rb") as f:
        reference_image_file = io.BytesIO(f.read())
    reference_image = preprocess_image(reference_image_file)
    
    # 類似度を計算（この結果が numpy.float32 になっている可能性がある）
    similarity = calculate_image_similarity_percentage(target_image, reference_image)
    
    # 変換して Python の float 型にする
    similarity = float(similarity)
    
    return {
        "similarity": similarity,
        "latitude": 35.0,
        "longitude": 139.0
    }


from PIL import Image
import numpy as np
import requests
from io import BytesIO
import io
import torch
import clip
from scipy.spatial.distance import cosine
import cv2
import mediapipe as mp
import random
import math

############################
# Google Maps API で衛星画像取得
############################

googleapikey = 'AIzaSyAOGekLTXac8mySSw_pzWRkgwrCpqBjX04'

def get_satellite_image(lat, lon, zoom=15, size="600x600", api_key=googleapikey):
    """
    Google Static Maps API を用いて、指定lat/lon/zoom/sizeの
    衛星写真を取得し、PIL.Imageで返す
    """
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap"
        f"?center={lat},{lon}"
        f"&zoom={zoom}"
        f"&size={size}"
        f"&maptype=satellite"
        f"&key={api_key}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGB")
    else:
        raise Exception(f"Failed to fetch satellite image: {response.status_code}")


############################
# 擬似的な「超解像」処理 (OpenCV拡大)
############################

def enhance_resolution_cv2(image, scale=4):
    """
    Real-ESRGAN の代わりに、OpenCV のバイキュービック補間で拡大。
    PIL.Image → np.array → cv2.resize → PIL.Image の流れ。
    """
    img_np = np.array(image)  # shape: (H,W,3)
    h, w = img_np.shape[:2]
    new_h, new_w = h*scale, w*scale
    enlarged = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    return Image.fromarray(enlarged)


############################
# CLIPで画像特徴を取得 & 類似度計算
############################

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

def extract_features_clip(img_pil):
    """
    CLIPの前処理 + encode_image() により画像特徴をnp.arrayで返す
    """
    # PIL.Image -> Tensor
    img_tensor = clip_preprocess(img_pil).unsqueeze(0).to(device)
    with torch.no_grad():
        features = clip_model.encode_image(img_tensor)
    return features.cpu().numpy().flatten()

def calculate_similarity(vec1, vec2):
    """
    コサイン類似度 (0~1) を 1 - cosine距離 で算出し、floatで返す
    """
    # scipy.spatial.distance の cosine() は距離なので
    # 類似度 = 1 - distance
    dist = cosine(vec1, vec2)
    return 1.0 - dist


############################
# マルチスケール & ランダム探索
############################

def explore_optimized_area(lat, lon, initial_radius_km,
                           max_iterations=5, num_samples=10):
    """
    指定の中心 lat/lon 付近をマルチスケールでランダム探索し、
    取得した衛星画像をリストで返す。
    戻り値: [(PIL.Image, lat, lon), ...]
    """
    best_images = []
    radius_km = initial_radius_km

    # 地理座標変換の簡易換算: 1km ~ 0.009° (約1km/111)
    deg_per_km = 0.009

    # 重複チェック用
    visited_points = []

    for iter_i in range(max_iterations):
        step = radius_km / math.sqrt(num_samples)
        for _ in range(num_samples):
            # ランダムに +- step (km) → deg
            rand_lat = lat + random.uniform(-step, step) * deg_per_km
            rand_lon = lon + random.uniform(-step, step) * deg_per_km

            # ざっくり既訪問に近すぎるならスキップ
            skip_flag = False
            for (vl, vn) in visited_points:
                # 距離(度)を計算
                # ここでは単純にユークリッド(度同士)
                d = math.dist((rand_lat, rand_lon), (vl, vn))
                if d < step * deg_per_km / 2:
                    skip_flag = True
                    break
            if skip_flag:
                continue

            # 取得
            try:
                sat_img = get_satellite_image(rand_lat, rand_lon,
                                              zoom=random.choice([14,16,18]),
                                              size="600x600")
                visited_points.append((rand_lat, rand_lon))
                best_images.append((sat_img, rand_lat, rand_lon))
            except Exception as e:
                print(f"[WARNING] Skipping location {rand_lat:.5f},{rand_lon:.5f}: {e}")

        # 半径を半分にしてより狭い範囲を探索
        radius_km /= 2

    return best_images


############################
# 画像比較・検索
############################

def find_best_match(user_image_path):
    """
    ユーザ画像とマルチスケール探索で集めた衛星画像を比較し、
    最もCLIP類似度が高い画像を "擬似超解像" して出力するデモ。
    """
    # ユーザ画像をPIL.Imageで開く
    user_image = Image.open(user_image_path).convert("RGB")
    user_feature = extract_features_clip(user_image)

    # 初期探索座標（例: 東京駅付近 35.6895, 139.6917）
    # ここをランダムにする
    # LLMとかで、相手が興味のなさそうな場所に飛ばすとか？
    init_lat, init_lon = 35.6895, 139.6917

    # 探索
    satellite_images = explore_optimized_area(
        lat=init_lat,
        lon=init_lon,
        initial_radius_km=50,  # 50kmから開始
        max_iterations=5,
        num_samples=10
    )

    # 衛星画像ごとに類似度計算
    results = []
    for (sat_img, lat, lon) in satellite_images:
        sat_feature = extract_features_clip(sat_img)
        sim = calculate_similarity(user_feature, sat_feature)
        results.append((sat_img, lat, lon, sim))

    # 類似度でソート（高い順）
    results.sort(key=lambda x: x[3], reverse=True)
    best_img, best_lat, best_lon, best_score = results[0]

    # 擬似的な超解像
    best_img_enhanced = enhance_resolution_cv2(best_img, scale=4)

    # 結果を表示（コンソール）
    print(f"--- Best Match ---")
    print(f"Location: lat={best_lat:.5f}, lon={best_lon:.5f}")
    print(f"Similarity (CLIP cos): {best_score:.4f}")
    print("Saving result as: best_match_enhanced.jpg")

    # 画像保存例
    best_img_enhanced.save("best_match_enhanced.jpg")

def find_best_match_origin(user_image, lat, lon):
    """
    ユーザ画像とマルチスケール探索で集めた衛星画像を比較し、
    最もCLIP類似度が高い画像を "擬似超解像" して出力するデモ。

    引数:
        user_image (PIL.Image): ユーザが提供する画像
    """
    # 画像はすでにPIL.Imageになっているため、そのまま使用
    user_feature = extract_features_clip(user_image)

    # 探索
    satellite_images = explore_optimized_area(
        lat=init_lat,
        lon=init_lon,
        initial_radius_km=50,  # 50kmから開始
        max_iterations=5,
        num_samples=10
    )

    # 衛星画像ごとに類似度計算
    results = []
    for (sat_img, lat, lon) in satellite_images:
        sat_feature = extract_features_clip(sat_img)
        sim = calculate_similarity(user_feature, sat_feature)
        results.append((sat_img, lat, lon, sim))

    # 類似度でソート（高い順）
    results.sort(key=lambda x: x[3], reverse=True)
    best_img, best_lat, best_lon, best_score = results[0]

    # 擬似的な超解像
    best_img_enhanced = enhance_resolution_cv2(best_img, scale=4)

    # 結果を表示（コンソール）
    print(f"--- Best Match ---")
    print(f"Location: lat={best_lat:.5f}, lon={best_lon:.5f}")
    print(f"Similarity (CLIP cos): {best_score:.4f}")
    print("Saving result as: best_match_enhanced.jpg")

    # 画像保存例
    # best_img_enhanced.save("best_match_enhanced.jpg")
    return best_img_enhanced

############################
# メイン
############################

def main():
    user_image_path = "森和也_face.jpg"  # ここを自分の比較したい画像に変更
    find_best_match(user_image_path)

if __name__ == "__main__":
    main()

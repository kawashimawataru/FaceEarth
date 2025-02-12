from PIL import Image
import numpy as np
import requests
from io import BytesIO
import io
import torch
import clip
from scipy.spatial.distance import cosine
import cv2

# ここでは、画像をリサイズ + 類似率を計算する処理を実装


################################
# 画像のリサイズ
def preprocess_image(image_file):
    # image_file はファイルオブジェクトであることを想定
    image = Image.open(image_file)
    image = image.resize((256, 256))  # リサイズ
    return np.array(image)

################################
# 画像の類似度計算

# ピクセルごとの輝度値の差分の総和を用いた手法 

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

# CLIP(画像とテキストの意味を学習したモデル)
# 異なるカテゴリの画像間の意味的な距離を測る

# CLIPのモデルとトークナイザーをロード
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 画像を前処理
def get_clip_feature(image_input):
    """
    image_input は以下のどちらかを想定:
      - PIL.Image.Image オブジェクト
      - numpy.ndarray (高さ x 幅 x チャンネル)
    """
    # もし numpy.ndarray なら PIL.Image に変換
    if isinstance(image_input, np.ndarray):
        image_input = Image.fromarray(image_input)

    # もし "P" モードなどになっていたら "RGB" に変換（念のため）
    if image_input.mode != "RGB":
        image_input = image_input.convert("RGB")

    # CLIPの前処理を通してテンソルに変換
    image_tensor = preprocess(image_input).unsqueeze(0).to(device)

    # 画像特徴を推論
    with torch.no_grad():
        feature = model.encode_image(image_tensor)

    # ベクトルを flatten() して numpy配列に変換
    return feature.cpu().numpy().flatten()
# 画像の類似度を計算
def calculate_clip_similarity(img1_path, img2_path):
    vec1 = get_clip_feature(img1_path)
    vec2 = get_clip_feature(img2_path)
    similarity = 1 - cosine(vec1, vec2)  # コサイン類似度
    return similarity * 100  # パーセンテージで返す


################################
# 画像内の対応点を線で結んで可視化する


def draw_matches(img1, img2, max_matches=50):
    """
    img1, img2 は以下のいずれか:
      - ファイルオブジェクト (BytesIO など)
      - ファイルパス
    preprocess_image が内部で PIL→numpy変換をしている場合、最終的に numpy.ndarray になっているはず。
    """
    img1 = preprocess_image(img1)  # ここで numpy.ndarray になる想定
    img2 = preprocess_image(img2)

    # 1. 特徴点検出
    orb = cv2.ORB_create()
    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)

    # 2. マッチング
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)

    # 3. 距離が小さい順にソート
    matches = sorted(matches, key=lambda x: x.distance)

    # 4. 上位 max_matches 個を線で描画
    matched_image = cv2.drawMatches(
        img1, kp1, img2, kp2, matches[:max_matches], None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    # ★★ 5. PNG バイナリにエンコードして return ★★
    success, encoded_png = cv2.imencode(".png", matched_image)
    if not success:
        raise ValueError("Failed to encode matched image to PNG.")

    return encoded_png.tobytes()


################################
# 類似度アウトプット

def find_most_similar_image(target_image_file, target_image_file2):
    target_image = preprocess_image(target_image_file)
    target_image2 = preprocess_image(target_image_file2)
    
    # 類似度を計算
    # 輝度値の差分による手法
    # similarity = calculate_image_similarity_percentage(target_image, reference_image)

    # CLIPによる類似度計算
    similarity = calculate_clip_similarity(target_image, target_image2)
    
    # 変換して Python の float 型にする
    similarity = float(similarity)
    
    return {
        "similarity": similarity,
        "latitude": 35.0,
        "longitude": 139.0
    }


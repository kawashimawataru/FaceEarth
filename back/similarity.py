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
# Mediapipe を例にした顔ランドマーク検出

mp_face_mesh = mp.solutions.face_mesh

def get_face_landmarks(image_array_rgb):
    """
    入力: RGB形式 (H,W,3) の numpy配列（PIL→np.arrayしたもの）
    出力: 顔ランドマークのリスト (x,y 座標; 0~W, 0~H のピクセル座標)
    """
    h, w, _ = image_array_rgb.shape
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,       # 目・唇などを精密にとる
        min_detection_confidence=0.5
    ) as face_mesh:
        # 画像を入力
        results = face_mesh.process(image_array_rgb)
        if not results.multi_face_landmarks:
            return []

        # 今回は1人分と仮定して先頭だけ取得
        face_landmarks = results.multi_face_landmarks[0]

        # 座標をpixel単位に変換
        landmark_points = []
        for lm in face_landmarks.landmark:
            x_px = int(lm.x * w)
            y_px = int(lm.y * h)
            landmark_points.append((x_px, y_px))

        return landmark_points

def get_jaw_contour_points(landmarks):
    """
    - Mediapipeの顔ランドマーク(468点想定)のうち、
      アゴ(輪郭)に相当するインデックスを抽出して返す。

    通常、0~16が「アゴライン」として取得できる場合が多い。
    (正確にはMediapipeのバージョンによっても変わる)

    ここでは簡易に [0..16] の17点を「顔輪郭」と仮定。
    """
    jaw_indexes = list(range(0, 17))  # 0〜16番がアゴライン
    contour = []
    for i in jaw_indexes:
        if i < len(landmarks):
            contour.append(landmarks[i])
    return contour

def pick_random_points_in_land(land_rgb, num_points):
    """土地画像の中でランダム座標を num_points 点抽出"""
    h, w, _ = land_rgb.shape
    points = []
    for _ in range(num_points):
        x = np.random.randint(0, w)
        y = np.random.randint(0, h)
        points.append((x,y))
    return points
   
def draw_artistic_matches(face_rgb, land_rgb, face_points, land_points):
    """顔画像と土地画像を左右に並べ、同数の点を線で結ぶ"""
    bgr_face = cv2.cvtColor(face_rgb, cv2.COLOR_RGB2BGR)
    bgr_land = cv2.cvtColor(land_rgb, cv2.COLOR_RGB2BGR)
    combined = np.concatenate([bgr_face, bgr_land], axis=1)
    offset = bgr_face.shape[1]

    # 点と線を描画
    for (fx, fy), (lx, ly) in zip(face_points, land_points):
        color = (
            np.random.randint(0, 255),
            np.random.randint(0, 255),
            np.random.randint(0, 255),
        )
        cv2.circle(combined, (fx, fy), 4, color, -1)
        cv2.circle(combined, (lx + offset, ly), 4, color, -1)
        cv2.line(combined, (fx, fy), (lx + offset, ly), color, 2)

    # PNGエンコード
    success, encoded_png = cv2.imencode(".png", combined)
    if not success:
        raise ValueError("Failed to encode PNG.")
    return encoded_png.tobytes()

def find_similar_land_point(x_f, y_f, face_rgb, land_rgb, search_radius=10, alpha=0.5):
    """
    - 顔画像 face_rgb 上の座標 (x_f, y_f) と同じ付近の土地画像 land_rgb の範囲を探索
    - 「座標が近く & 色差が小さい」ピクセルを返す
      スコア = 距離 + alpha*色差
    - search_radius: 周囲 ±この値 の範囲を走査
    - alpha: 色差にかける重み (大きいほど色を重視)
    """
    h_land, w_land, _ = land_rgb.shape
    h_face, w_face, _ = face_rgb.shape

    # 顔が範囲外ならそのまま返す
    if not (0 <= x_f < w_face and 0 <= y_f < h_face):
        return x_f, y_f

    face_color = face_rgb[y_f, x_f]

    # 検索範囲を設定
    x_min = max(0, x_f - search_radius)
    x_max = min(w_land - 1, x_f + search_radius)
    y_min = max(0, y_f - search_radius)
    y_max = min(h_land - 1, y_f + search_radius)

    best_score = float('inf')
    best_point = (x_f, y_f)
    for yy in range(y_min, y_max+1):
        for xx in range(x_min, x_max+1):
            land_color = land_rgb[yy, xx]
            # 座標差
            dist_coord = math.sqrt((x_f - xx)**2 + (y_f - yy)**2)
            # 色差 (RGB)
            dist_color = math.sqrt(
                (float(face_color[0]) - float(land_color[0]))**2 +
                (float(face_color[1]) - float(land_color[1]))**2 +
                (float(face_color[2]) - float(land_color[2]))**2
            )
            score = dist_coord + alpha*dist_color
            if score < best_score:
                best_score = score
                best_point = (xx, yy)

    return best_point
################################
# 画像内の対応点を線で結んで可視化する

import random

def draw_matches(face_file, land_file,
                 max_points=10,     # 全顔ランドマークからのサンプリング数
                 search_radius=10,  # 近傍探索の半径
                 alpha=0.5,         # 色差重み
                 highlight_jaw=True # 顔輪郭を強調表示するか
                 ):
    """
    - 顔画像と土地画像を読み込み、Mediapipeで顔ランドマークを取得
    - そのうち max_points 個をサンプリング
    - 各ランドマーク (x_f, y_f) に対し、土地画像内の「座標が近く、色差が小さい」点を探索
    - 左右に画像を並べ、線で結ぶ
    - 顔輪郭(アゴライン)を別扱いで太線 or 同じ座標近傍に描画
    - PNGバイナリを返す
    """
    # 1) 画像をRGBで読み込み (256x256)
    face_rgb = preprocess_image(face_file)
    land_rgb = preprocess_image(land_file)

    # 2) 顔ランドマーク取得
    face_landmarks = get_face_landmarks(face_rgb)
    if not face_landmarks:
        # 顔が検出できない場合、仮に3点
        face_landmarks = [(60,60), (120,120), (100,70)]

    # 3) ランドマーク多すぎる場合はサンプリング
    n_points = len(face_landmarks)
    if n_points > max_points:
        face_landmarks = random.sample(face_landmarks, max_points)
        n_points = max_points

    # (オプション) 顔輪郭 (jaw line) のインデックスだけ別途取得
    # ここでは "元の" ランドマーク全体に対して抽出しているので
    # サンプリングとは関係なく、jaw lineを表示したい場合
    jaw_points = []
    if highlight_jaw and len(face_landmarks) >= 17:
        # 本来は "元の468点" から顎ラインを取りたいため、
        # face_landmarks が既にサンプリングされたものならうまく取れない可能性があります。
        # → ここでは簡易対応として、「サンプリング前に」もう1回全体を読み直すなどするか、
        #    もしくは get_jaw_contour_points(...) にサンプリング前のリストを渡す。
        #    今回は単純化のためにサンプリング後のリストを対象に jaw_line っぽい部分を取ります。
        jaw_points = face_landmarks[:17]  # 先頭17点を"アゴライン"とみなす (かなり簡易)
        # 本格的には "元の468点" → get_jaw_contour_points → 17点 という流れがおすすめ。

    # 4) 描画用に BGR 画像を用意し、左右に並べる
    bgr_face = cv2.cvtColor(face_rgb, cv2.COLOR_RGB2BGR)
    bgr_land = cv2.cvtColor(land_rgb, cv2.COLOR_RGB2BGR)
    combined = np.concatenate([bgr_face, bgr_land], axis=1)  # shape=(256,512,3)
    offset = bgr_face.shape[1]

    # 5) 各ランドマークを土地側に対応づけて線を引く
    for (x_f, y_f) in face_landmarks:
        # (a) 顔の近傍にある "似た" 土地座標を探す
        x_l, y_l = find_similar_land_point(
            x_f, y_f,
            face_rgb, land_rgb,
            search_radius=search_radius, alpha=alpha
        )
        color = (
            np.random.randint(0,255),
            np.random.randint(0,255),
            np.random.randint(0,255)
        )
        # (b) 左画像に丸、右画像に丸、その間を線で結ぶ
        cv2.circle(combined, (x_f, y_f), 4, color, -1)
        cv2.circle(combined, (x_l+offset, y_l), 4, color, -1)
        cv2.line(combined, (x_f, y_f), (x_l+offset, y_l), color, 2)

    # 6) 顔輪郭を強調表示
    #    (サンプリング後の先頭17点を輪郭とし、同様に対応づけ)
    if highlight_jaw and len(jaw_points) > 1:
        jaw_color = (0, 255, 255)  # 黄色
        thickness = 3
        # 複数の連続点を線で結ぶ (アゴライン)
        for i in range(len(jaw_points)-1):
            (x0, y0) = jaw_points[i]
            (x1, y1) = jaw_points[i+1]
            # 顔側を太線で結ぶ
            cv2.line(combined, (x0, y0), (x1, y1), jaw_color, thickness)
            # 土地側も "対応する座標" を探して輪郭っぽく結ぶ
            (xl0, yl0) = find_similar_land_point(x0, y0, face_rgb, land_rgb,
                                                 search_radius, alpha)
            (xl1, yl1) = find_similar_land_point(x1, y1, face_rgb, land_rgb,
                                                 search_radius, alpha)
            cv2.line(combined, (xl0+offset, yl0), (xl1+offset, yl1), jaw_color, thickness)

    # 7) PNGエンコードしてバイナリ返却
    success, encoded_png = cv2.imencode(".png", combined)
    if not success:
        raise ValueError("Failed to encode combined image to PNG.")
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


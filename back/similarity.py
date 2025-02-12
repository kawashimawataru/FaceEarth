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


############################
# ヘルパー関数
############################

def preprocess_image(image_file):
    """画像ファイル(パス or BytesIO)を256x256にリサイズ→RGB配列"""
    pil_img = Image.open(image_file).resize((256,256))
    return np.array(pil_img)  # shape=(256,256,3)

def get_edges(image_rgb, t1=100, t2=200):
    """Canny輪郭(0/255)取得"""
    bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    edges = cv2.Canny(bgr, t1, t2)
    return edges

def find_all_contours(edges):
    """
    edges: 0/255の2値画像
    戻り値: contours(list of numpy.ndarray), hierarchy
    """
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, hierarchy

def sample_contour_points(contour, step_length=5.0):
    """
    輪郭 contour(形=(N,1,2)) をアーク長に沿って step_length おきにサンプリング
    戻り値: 点列 [(x1,y1), (x2,y2), ...]
    """
    if contour is None or len(contour) < 2:
        return []
    total_length = 0.0
    dists = []
    for i in range(len(contour)-1):
        x0,y0 = contour[i][0]
        x1,y1 = contour[i+1][0]
        seg_len = math.dist((x0,y0),(x1,y1))
        dists.append(seg_len)
        total_length += seg_len

    points = []
    if len(contour)>0:
        x0,y0 = contour[0][0]
        points.append((x0,y0))

    step_count = int(total_length // step_length)
    idx = 0
    dist_idx = 0.0

    for _ in range(step_count):
        target_len = len(points)*step_length
        while idx < len(dists):
            seg = dists[idx]
            if dist_idx + seg < target_len:
                dist_idx += seg
                idx += 1
            else:
                remain = target_len - dist_idx
                ratio = remain / seg
                xA,yA = contour[idx][0]
                xB,yB = contour[idx+1][0]
                x_samp = xA + ratio*(xB-xA)
                y_samp = yA + ratio*(yB-yA)
                points.append((int(x_samp), int(y_samp)))
                break
    return points

def extract_subcontour(points, start_idx, length):
    """点列から連続する length 個を取り出す"""
    end_idx = min(start_idx+length, len(points))
    return points[start_idx:end_idx]

def compute_average_distance(segmentA, segmentB):
    """
    2つの同長点列の平均距離
    """
    if len(segmentA)!=len(segmentB) or len(segmentA)==0:
        return float('inf')
    dsum=0.0
    for (ax,ay),(bx,by) in zip(segmentA,segmentB):
        dsum+= math.dist((ax,ay),(bx,by))
    return dsum/len(segmentA)



################################
# 画像内の対応点を線で結んで可視化する

import random

def draw_matches(face_file, land_file,
                 face_canny1=100,  # 顔のエッジ検出最小しきい値 (低いと輪郭が増え、高いと簡略化),デフォルト100
                 face_canny2=150,  # 顔のエッジ検出最大しきい値 (低いと輪郭が増え、高いと簡略化),デフォルト200
                 land_canny1=100,  # 土地のエッジ検出最小しきい値 (低いと輪郭が増え、高いと簡略化),デフォルト100
                 land_canny2=150,  # 土地のエッジ検出最大しきい値 (低いと輪郭が増え、高いと簡略化),デフォルト200
                 step_length=3.0,  # 輪郭のサンプリング間隔 (小さいと詳細、多いと全体を大まかに捉える),デフォルト5.0
                 segment_size=5,   # サブ区間の長さ (大きいと広範囲、小さいと細かい特徴を捉える),デフォルト20
                 max_search=100):  # 比較する最大サブ区間数 (大きいと適切なマッチング精度UP、処理時間増),デフォルト50
    """

    1) 顔: findContours → すべての輪郭を緑表示
       (線で結ぶのではなくピクセル単位)
    2) 土地: findContours → 複数輪郭を「マッチング用」にまとめてサンプリング
    3) 顔輪郭(複数)をサンプリングし、サブ区間ごとに
       土地輪郭のサブ区間(全候補)と比較 → 距離が最小の部分をマゼンタ表示
    """

    # A) 読み込み
    face_img = preprocess_image(face_file)
    land_img = preprocess_image(land_file)
    h,w,_ = face_img.shape

    # B) Canny
    face_edges = get_edges(face_img, face_canny1, face_canny2)
    land_edges = get_edges(land_img, land_canny1, land_canny2)

    # C) 全輪郭取得
    face_contours,_ = find_all_contours(face_edges)
    land_contours,_ = find_all_contours(land_edges)

    # 描画用
    bgr_face = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
    bgr_land = cv2.cvtColor(land_img, cv2.COLOR_RGB2BGR)
    combined = np.concatenate([bgr_face, bgr_land], axis=1)
    offset = bgr_face.shape[1]

    # 1) 顔輪郭はすべて緑表示 (ピクセル単位)
    for y in range(h):
        for x in range(w):
            if face_edges[y,x]>0:
                combined[y,x]=(0,255,0)

    # 2) 土地側の輪郭を "サンプリング用" に1つの大きいリストにまとめる
    #    もしくは輪郭ごとに保管してサブ区間比較してもOKだが、複雑なので簡易化
    land_points_all=[]
    for c in land_contours:
        c_samp = sample_contour_points(c, step_length=step_length)
        land_points_all.extend(c_samp)

    if len(land_points_all) < segment_size:
        # 土地側の輪郭が短すぎる
        success,enc = cv2.imencode(".png", combined)
        return enc.tobytes()

    land_sub_count = max(0, len(land_points_all)-segment_size)

    # 3) 顔輪郭ごとにサンプリング & サブ区間化 → 土地側と比較
    for face_c in face_contours:
        # サンプリング
        face_points_samp = sample_contour_points(face_c, step_length=step_length)
        if len(face_points_samp)<segment_size:
            continue

        face_sub_count = len(face_points_samp)-segment_size
        face_sub_count = min(face_sub_count, max_search)  # 過度な計算を防ぐ

        # 各サブ区間
        for i in range(face_sub_count):
            subA = extract_subcontour(face_points_samp, i, segment_size)
            best_j=0
            best_dist=float('inf')

            # 土地側サブ区間全探索
            for j in range(land_sub_count):
                subB = extract_subcontour(land_points_all,j,segment_size)
                dist=compute_average_distance(subA,subB)
                if dist<best_dist:
                    best_dist=dist
                    best_j=j

            # 最小distだったサブ区間をマゼンタ表示
            subB= extract_subcontour(land_points_all,best_j,segment_size)
            for (xL,yL) in subB:
                if 0<=xL<w and 0<=yL<h:
                    combined[yL,xL+offset]=(255,0,255)

    # 最後にPNG
    success,encoded = cv2.imencode(".png", combined)
    if not success:
        raise ValueError("Failed to encode final image.")
    return encoded.tobytes()

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


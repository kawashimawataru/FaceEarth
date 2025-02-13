import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from sklearn.metrics.pairwise import cosine_similarity
from torchvision import transforms
from torchvision.models import resnet50
from realesrgan import RealESRGAN
import os
from sentence_transformers import SentenceTransformer
import random
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# Google Maps API から画像を取得する関数
def get_satellite_image(lat, lon, zoom=15, size="600x600", api_key="YOUR_GOOGLE_API_KEY"):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}&maptype=satellite&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(f"Failed to fetch the image from Google Maps API: {response.status_code}")

# 画像を超解像度化する関数（高スコアの画像のみ適用）
def enhance_resolution(image):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = 'weights/RealESRGAN_x4.pth'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Real-ESRGAN model weights not found at {model_path}")
    model = RealESRGAN(device, scale=4)
    model.load_weights(model_path)
    return model.predict(image)

# 画像の特徴を抽出する関数（ResNet50を使用）
def extract_features(img, model):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img_tensor = transform(img).unsqueeze(0).to(next(model.parameters()).device)
    with torch.no_grad():
        features = model(img_tensor)
    return features.view(-1).cpu().numpy()

# 類似度を計算する関数
def calculate_similarity(features1, features2):
    return cosine_similarity([features1], [features2])[0][0]

# ResNet50モデルをロード
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet_model = resnet50(pretrained=True).eval().to(device)

# 探索済みポイントを効率的に管理するためのKDTree
def build_kdtree(points):
    return KDTree(points) if points else None

# 探索の可視化
def plot_explored_areas(points):
    if points:
        lats, lons = zip(*points)
        plt.scatter(lons, lats, marker='o', color='red')
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Explored Locations")
        plt.show()

# マルチスケール & アクティブ探索による広範囲探索
def explore_optimized_area(lat, lon, initial_radius_km, max_iterations=5, num_samples=10):
    best_images = []
    radius_km = initial_radius_km
    explored_points = []
    kdtree = None
    for _ in range(max_iterations):
        step = radius_km / np.sqrt(num_samples)
        for _ in range(num_samples):
            new_lat = lat + random.uniform(-step, step) * 0.009
            new_lon = lon + random.uniform(-step, step) * 0.009
            if kdtree and kdtree.query([new_lat, new_lon])[0] < step * 0.009:
                continue
            try:
                img = get_satellite_image(new_lat, new_lon, zoom=random.choice([14, 16, 18]))
                explored_points.append((new_lat, new_lon))
                kdtree = build_kdtree(explored_points)
                best_images.append((img, new_lat, new_lon))
            except Exception as e:
                print(f"Skipping location ({new_lat}, {new_lon}): {e}")
        radius_km /= 2
    plot_explored_areas(explored_points)
    return best_images

# 画像の比較・検索（超解像度適用は上位候補のみ）
def find_best_match(user_image_path):
    user_image = Image.open(user_image_path).convert("RGB")
    user_features = extract_features(user_image, resnet_model)
    
    initial_lat, initial_lon = 35.6895, 139.6917  # 初期探索座標（例: 東京）
    satellite_images = explore_optimized_area(initial_lat, initial_lon, initial_radius_km=50)
    
    best_matches = []
    for img, lat, lon in satellite_images:
        image_features = extract_features(img, resnet_model)
        score = calculate_similarity(user_features, image_features)
        best_matches.append((img, lat, lon, score))
    
    best_matches.sort(key=lambda x: x[3], reverse=True)
    best_image, best_lat, best_lon, best_score = best_matches[0]
    best_image = enhance_resolution(best_image)
    
    best_image.show()
    print(f"Best match found at: {best_lat}, {best_lon} with similarity score: {best_score}")

# 実行例
user_image_path = input("Enter the path to your image: ")
find_best_match(user_image_path)

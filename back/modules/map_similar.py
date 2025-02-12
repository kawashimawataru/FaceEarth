import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from sklearn.metrics.pairwise import cosine_similarity
from torchvision import transforms
from torchvision.models import vgg16
from realesrgan import RealESRGAN

# Google Maps API から画像を取得する関数
def get_satellite_image(lat, lon, zoom=15, size="600x600", api_key="YOUR_GOOGLE_API_KEY"):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}&maptype=satellite&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception("Failed to fetch the image from Google Maps API")

# 画像を超解像度化する関数
def enhance_resolution(image):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth')
    return model.predict(image)

# 画像の特徴を抽出する関数
def extract_features(img, model):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        features = model(img_tensor)
    return features.view(-1).numpy()

# 類似度を計算する関数
def calculate_similarity(image1, image2, model):
    features1 = extract_features(image1, model)
    features2 = extract_features(image2, model)
    return cosine_similarity([features1], [features2])[0][0]

# VGG16モデルをロード
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vgg_model = vgg16(pretrained=True).features.eval().to(device)

# テスト用の画像（顔画像）を読み込む
face_image = Image.open("face_image.jpg")

# Google Maps API で取得した衛星画像
satellite_image = get_satellite_image(35.6895, 139.6917)

# 超解像度化
sr_satellite_image = enhance_resolution(satellite_image)

# 画像の類似度を計算
similarity_score = calculate_similarity(face_image, sr_satellite_image, vgg_model)
print(f"Similarity Score: {similarity_score}")

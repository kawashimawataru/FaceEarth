"""パイプライン全体の定数。

MODEL_ID / EMBED_DIM / TILE_URL_TEMPLATE は web/src/lib/config.ts と対 (データ契約)。
変更したら必ず両方を揃えて全ステージを再実行すること。
"""

from pathlib import Path

# ブラウザ側は Xenova/clip-vit-base-patch32 (同一重みの ONNX 版)
MODEL_ID = "openai/clip-vit-base-patch32"
EMBED_DIM = 512

# EOX Sentinel-2 Cloudless 2016 (CC-BY 4.0)
TILE_URL_TEMPLATE = (
    "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/"
    "default/GoogleMapsCompatible/{z}/{y}/{x}.jpg"
)

ZOOM = 7
# 高緯度の氷原ノイズを除く。北はアイスランド・スカンジナビアを残し、
# 南は南極大陸を丸ごと外す (南極周縁は逆ジオコーディングも破綻するため)
MAX_LAT = 70.0
MIN_LAT = -60.0

ROOT = Path(__file__).parent
DATA = ROOT / "data"            # gitignore 済み (キャッシュ・中間生成物)
CACHE = DATA / "tiles"          # ダウンロードしたタイル JPEG
OUT_WEB = ROOT.parent / "web" / "public" / "data"  # 最終成果物の出力先

CANDIDATES_JSON = DATA / "tiles_candidate.json"   # 01 の出力: 陸地タイル一覧
FILTERED_JSON = DATA / "tiles_filtered.json"      # 03 の出力: 画素フィルタ後
EMBEDDINGS_BIN = OUT_WEB / "embeddings.bin"       # 04 の出力 (fp16, N×EMBED_DIM)
META_JSON = OUT_WEB / "tiles.meta.json"           # 05 の出力

# 開発時の小規模サンプル実行: python 01_list_tiles.py --sample
SAMPLE_REGIONS = [
    # (名前, lat_min, lat_max, lng_min, lng_max) — 気候の異なる地域を少しずつ
    ("japan", 30.0, 45.0, 129.0, 146.0),
    ("sahara", 18.0, 28.0, -5.0, 15.0),
    ("alps", 44.0, 48.0, 5.0, 15.0),
    ("amazon", -8.0, 2.0, -70.0, -55.0),
]

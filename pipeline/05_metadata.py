"""tiles_embedded.json の各タイルに地名と地形特徴タグを付け、tiles.meta.json を書く。

- 地名: reverse_geocoder (オフライン, GeoNames ベース) → 国コード + admin1
  国名は country_ja.py で日本語化 (無ければコードのまま)
- traits: タイル画像の画素統計から desert/forest/mountain/coast/ice/plain を推定
出力順は embeddings.bin の行順と一致する (i フィールド)。
"""

import json

import numpy as np
import reverse_geocoder as rg
from PIL import Image

from config import DATA, META_JSON

from country_ja import COUNTRY_JA

from importlib import import_module

tile_path = import_module("02_download_tiles").tile_path

EMBEDDED_JSON = DATA / "tiles_embedded.json"


def traits_for(img: Image.Image) -> list[str]:
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    brightness = a.mean()
    green_frac = float(((g > r) & (g > b + 5)).mean())
    blue_frac = float(((b > r + 10) & (b > g + 5)).mean())
    # 「白」は無彩色に限る (明るい砂漠を雪と誤判定しないよう、R-B の彩度差で除く)
    white_frac = float(((a.min(axis=2) > 190) & (np.abs(r - b) < 18)).mean())
    warm_frac = float(((r > b + 20) & (g > b + 10)).mean())
    # 起伏感: 輝度勾配の平均 (山岳・渓谷はテクスチャが強い)
    gray = a.mean(axis=2)
    gy, gx = np.gradient(gray)
    texture = float(np.hypot(gx, gy).mean())

    traits: list[str] = []
    if white_frac > 0.25:
        traits.append("ice")
    if green_frac > 0.30:
        traits.append("forest")
    if warm_frac > 0.45 and brightness > 120 and green_frac < 0.15:
        traits.append("desert")
    if texture > 14.0:
        traits.append("mountain")
    if 0.08 < blue_frac < 0.60:
        traits.append("coast")
    if not traits:
        traits.append("plain")
    return traits[:3]


def main() -> None:
    tiles = json.loads(EMBEDDED_JSON.read_text())
    # reverse_geocoder はバッチが速い
    coords = [(t["lat"], t["lng"]) for t in tiles]
    geo = rg.search(coords)

    metas = []
    for i, (t, g) in enumerate(zip(tiles, geo)):
        with Image.open(tile_path(t["z"], t["x"], t["y"])) as img:
            traits = traits_for(img)
        cc = g.get("cc", "")
        metas.append(
            {
                "i": i,
                "z": t["z"],
                "x": t["x"],
                "y": t["y"],
                "lat": round(t["lat"], 5),
                "lng": round(t["lng"], 5),
                "country": COUNTRY_JA.get(cc, cc),
                "region": g.get("admin1", ""),
                "traits": traits,
            }
        )
        if (i + 1) % 500 == 0:
            print(f"meta {i + 1}/{len(tiles)}")

    META_JSON.write_text(json.dumps(metas, ensure_ascii=False))
    print(f"wrote {META_JSON} ({len(metas)} tiles, {META_JSON.stat().st_size/1e3:.0f} KB)")


if __name__ == "__main__":
    main()

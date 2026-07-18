"""ダウンロード済みタイルから「ほぼ一様な海・無地」タイルを除外して tiles_filtered.json を書く。

海タイルの特徴: 彩度・輝度の分散が極端に小さい / 青が支配的で変化がない。
判定はシンプルに「画素標準偏差」と「青優勢率」の組み合わせ。
"""

import json

import numpy as np
from PIL import Image

from config import CANDIDATES_JSON, FILTERED_JSON

from importlib import import_module

tile_path = import_module("02_download_tiles").tile_path

# 経験的しきい値: std がこれ未満なら「一様タイル」(海・雲・氷原の無地)
STD_MIN = 12.0
# 青(B > R かつ B > G)画素がこの率を超え、かつ std が低めなら海とみなす
BLUE_FRAC_MAX = 0.85
STD_OCEAN = 25.0


def is_boring(img: Image.Image) -> bool:
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    std = a.std(axis=(0, 1)).mean()
    if std < STD_MIN:
        return True
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    blue_frac = float(((b > r) & (b > g)).mean())
    return blue_frac > BLUE_FRAC_MAX and std < STD_OCEAN


def main() -> None:
    tiles = json.loads(CANDIDATES_JSON.read_text())
    kept = []
    dropped = 0
    for t in tiles:
        path = tile_path(t["z"], t["x"], t["y"])
        if not path.exists():
            dropped += 1
            continue
        try:
            with Image.open(path) as img:
                if is_boring(img):
                    dropped += 1
                    continue
        except OSError:
            dropped += 1
            continue
        kept.append(t)
    FILTERED_JSON.write_text(json.dumps(kept))
    print(f"kept {len(kept)} / dropped {dropped}")


if __name__ == "__main__":
    main()

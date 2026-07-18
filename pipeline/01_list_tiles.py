"""z=ZOOM の全タイルを列挙し、陸地を含むものだけを tiles_candidate.json に書き出す。

陸判定: タイル内 5 点 (中心+四隅寄り) のいずれかが global-land-mask で陸なら採用。
--sample で config.SAMPLE_REGIONS の範囲だけに絞る (開発用)。
"""

import json
import sys

import numpy as np
from global_land_mask import globe

from config import CANDIDATES_JSON, DATA, MAX_ABS_LAT, SAMPLE_REGIONS, ZOOM
from tile_math import tile_center, tile_sample_points


def in_sample_regions(lat: float, lng: float) -> bool:
    return any(
        la0 <= lat <= la1 and lo0 <= lng <= lo1
        for _, la0, la1, lo0, lo1 in SAMPLE_REGIONS
    )


def main() -> None:
    sample = "--sample" in sys.argv
    n = 2**ZOOM
    tiles = []
    for y in range(n):
        lat_c, _ = tile_center(ZOOM, 0, y)
        if abs(lat_c) > MAX_ABS_LAT:
            continue
        for x in range(n):
            lat, lng = tile_center(ZOOM, x, y)
            if sample and not in_sample_regions(lat, lng):
                continue
            pts = tile_sample_points(ZOOM, x, y)
            lats = np.array([p[0] for p in pts])
            lngs = np.array([p[1] for p in pts])
            if globe.is_land(lats, lngs).any():
                tiles.append({"z": ZOOM, "x": x, "y": y, "lat": lat, "lng": lng})

    DATA.mkdir(parents=True, exist_ok=True)
    CANDIDATES_JSON.write_text(json.dumps(tiles))
    print(f"candidates: {len(tiles)} tiles (zoom={ZOOM}, sample={sample})")


if __name__ == "__main__":
    main()

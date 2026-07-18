"""Web Mercator タイル座標の数学 (web/src/lib/tiles.ts と同一の定義)"""

import math


def tile2lng(x: float, z: int) -> float:
    return x / 2**z * 360.0 - 180.0


def tile2lat(y: float, z: int) -> float:
    n = math.pi - 2.0 * math.pi * y / 2**z
    return math.degrees(math.atan(0.5 * (math.exp(n) - math.exp(-n))))


def tile_center(z: int, x: int, y: int) -> tuple[float, float]:
    """(lat, lng) タイル中心"""
    return (
        (tile2lat(y, z) + tile2lat(y + 1, z)) / 2,
        (tile2lng(x, z) + tile2lng(x + 1, z)) / 2,
    )


def tile_sample_points(z: int, x: int, y: int) -> list[tuple[float, float]]:
    """陸判定用: 中心 + 四隅寄りの 4 点 (計 5 点) の (lat, lng)"""
    pts = []
    for fx, fy in [(0.5, 0.5), (0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]:
        pts.append((tile2lat(y + fy, z), tile2lng(x + fx, z)))
    return pts

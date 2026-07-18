/**
 * 顔ランドマーク ⇔ 衛星タイルの対応点探索。
 * 旧 back/similarity.py の find_similar_land_point の移植 + 改善:
 * - スコア = 座標距離 + alpha × 色距離 (原典どおり)
 * - 改善: Sobel 勾配の強い画素 (海岸線・尾根) にボーナスを与え、線が地形の特徴に着地するように
 * - 乱数はタイル ID シードで決定的 (同じ顔×同じ場所なら同じアートになる)
 */

export interface Pt {
  x: number;
  y: number;
}

/** mulberry32 — 決定的な軽量 PRNG */
export function seededRandom(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export interface LandField {
  width: number;
  height: number;
  /** RGBA 画素 */
  data: Uint8ClampedArray;
  /** 画素ごとの勾配強度 (0..1 正規化) */
  gradient: Float32Array;
}

/** タイル画像から画素と Sobel 勾配場を作る */
export function buildLandField(imageData: ImageData): LandField {
  const { width, height, data } = imageData;
  const gray = new Float32Array(width * height);
  for (let i = 0; i < width * height; i++) {
    gray[i] = (data[i * 4] + data[i * 4 + 1] + data[i * 4 + 2]) / 3;
  }
  const gradient = new Float32Array(width * height);
  let maxG = 1;
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      const i = y * width + x;
      const gx =
        gray[i - width + 1] + 2 * gray[i + 1] + gray[i + width + 1] -
        gray[i - width - 1] - 2 * gray[i - 1] - gray[i + width - 1];
      const gy =
        gray[i + width - 1] + 2 * gray[i + width] + gray[i + width + 1] -
        gray[i - width - 1] - 2 * gray[i - width] - gray[i - width + 1];
      const g = Math.hypot(gx, gy);
      gradient[i] = g;
      if (g > maxG) maxG = g;
    }
  }
  for (let i = 0; i < gradient.length; i++) gradient[i] /= maxG;
  return { width, height, data, gradient };
}

/**
 * 顔側の点 (fx, fy) と色が近く、地形の特徴 (勾配) がある土地側の点を探す。
 * faceColor: その点の顔画素 RGB。座標は両画像とも同じ正方形スケールを想定。
 */
export function findSimilarLandPoint(
  fx: number,
  fy: number,
  faceColor: [number, number, number],
  land: LandField,
  searchRadius = 26,
  alpha = 0.35,
  gradientBonus = 30,
): Pt {
  const x0 = Math.max(1, Math.round(fx) - searchRadius);
  const x1 = Math.min(land.width - 2, Math.round(fx) + searchRadius);
  const y0 = Math.max(1, Math.round(fy) - searchRadius);
  const y1 = Math.min(land.height - 2, Math.round(fy) + searchRadius);

  let best: Pt = { x: Math.round(fx), y: Math.round(fy) };
  let bestScore = Infinity;
  for (let y = y0; y <= y1; y++) {
    for (let x = x0; x <= x1; x++) {
      const i = y * land.width + x;
      const dr = faceColor[0] - land.data[i * 4];
      const dg = faceColor[1] - land.data[i * 4 + 1];
      const db = faceColor[2] - land.data[i * 4 + 2];
      const distColor = Math.sqrt(dr * dr + dg * dg + db * db);
      const distCoord = Math.hypot(fx - x, fy - y);
      const score = distCoord + alpha * distColor - gradientBonus * land.gradient[i];
      if (score < bestScore) {
        bestScore = score;
        best = { x, y };
      }
    }
  }
  return best;
}

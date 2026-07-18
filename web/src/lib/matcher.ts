/**
 * 事前計算した衛星タイル埋め込み(fp16)を読み込み、
 * 顔埋め込みとの総当たり cosine 類似度で top-K を返す。
 * N≈5,000 × 512 次元なら素の JS で数 ms。
 */

import { EMBED_DIM, EMBEDDINGS_URL, TILES_META_URL, TOP_K } from "./config";
import type { TileMeta } from "./tiles";

export interface MatchResult {
  meta: TileMeta;
  /** 生の cosine 類似度 (-1..1) */
  cosine: number;
  /** コーパス全体で min-max 正規化した表示用スコア (0..100)。相対値。 */
  resonance: number;
  /** 順位 (1 始まり) */
  rank: number;
}

export interface Corpus {
  /** 行ごとに L2 正規化済み、N×EMBED_DIM */
  vectors: Float32Array;
  metas: TileMeta[];
  n: number;
}

/** fp16 (IEEE 754 half) → fp32。読み込み時に一度だけ変換する。 */
export function decodeFp16(src: Uint16Array): Float32Array {
  const out = new Float32Array(src.length);
  for (let i = 0; i < src.length; i++) {
    const h = src[i];
    const sign = (h & 0x8000) >> 15;
    const exp = (h & 0x7c00) >> 10;
    const frac = h & 0x03ff;
    let v: number;
    if (exp === 0) {
      v = frac * 2 ** -24; // 非正規化数
    } else if (exp === 0x1f) {
      v = frac ? NaN : Infinity;
    } else {
      v = (1 + frac / 1024) * 2 ** (exp - 15);
    }
    out[i] = sign ? -v : v;
  }
  return out;
}

let corpusPromise: Promise<Corpus> | null = null;

export function loadCorpus(): Promise<Corpus> {
  corpusPromise ??= (async () => {
    const [binRes, metaRes] = await Promise.all([
      fetch(EMBEDDINGS_URL),
      fetch(TILES_META_URL),
    ]);
    if (!binRes.ok || !metaRes.ok) {
      throw new Error("タイルデータの読み込みに失敗しました");
    }
    const [buf, metas] = await Promise.all([
      binRes.arrayBuffer(),
      metaRes.json() as Promise<TileMeta[]>,
    ]);
    const vectors = decodeFp16(new Uint16Array(buf));
    const n = vectors.length / EMBED_DIM;
    if (!Number.isInteger(n) || n !== metas.length) {
      throw new Error(
        `タイルデータが不整合です (embeddings: ${n} 行, meta: ${metas.length} 件)`,
      );
    }
    return { vectors, metas, n };
  })();
  return corpusPromise;
}

/**
 * クエリ(L2 正規化済み顔埋め込み)に対する top-K。
 * コーパスも正規化済みなので内積 = cosine。
 */
export function match(query: Float32Array, corpus: Corpus, k = TOP_K): MatchResult[] {
  const { vectors, metas, n } = corpus;
  const scores = new Float32Array(n);
  let min = Infinity;
  let max = -Infinity;
  for (let i = 0; i < n; i++) {
    let dot = 0;
    const base = i * EMBED_DIM;
    for (let j = 0; j < EMBED_DIM; j++) {
      dot += query[j] * vectors[base + j];
    }
    scores[i] = dot;
    if (dot < min) min = dot;
    if (dot > max) max = dot;
  }

  const order = Array.from({ length: n }, (_, i) => i)
    .sort((a, b) => scores[b] - scores[a])
    .slice(0, k);

  const range = max - min || 1;
  return order.map((idx, rank) => ({
    meta: metas[idx],
    cosine: scores[idx],
    resonance: ((scores[idx] - min) / range) * 100,
    rank: rank + 1,
  }));
}

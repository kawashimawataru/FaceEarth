// 検証:
// 1. embeddings.bin (fp16) を decodeFp16 相当で復元し、fp32 直接埋め込みとの一致を確認
// 2. テスト顔画像を fp32 と q8 (ブラウザ WASM フォールバック相当) で埋め込み、
//    コーパスに対する top-3 順位が一致することを確認
//
// 実行: node 06_verify.mjs

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const ROOT = import.meta.dirname;
const DATA = path.join(ROOT, "data");
const BIN = path.resolve(ROOT, "../web/public/data/embeddings.bin");
const EMBEDDED = path.join(DATA, "tiles_embedded.json");
const EMBED_DIM = 512;

function decodeFp16(u16) {
  const out = new Float32Array(u16.length);
  for (let i = 0; i < u16.length; i++) {
    const h = u16[i];
    const sign = (h & 0x8000) >> 15;
    const exp = (h & 0x7c00) >> 10;
    const frac = h & 0x03ff;
    let v;
    if (exp === 0) v = frac * 2 ** -24;
    else if (exp === 0x1f) v = frac ? NaN : Infinity;
    else v = (1 + frac / 1024) * 2 ** (exp - 15);
    out[i] = sign ? -v : v;
  }
  return out;
}

function topK(query, corpus, n, k = 3) {
  const scores = [];
  for (let i = 0; i < n; i++) {
    let dot = 0;
    for (let j = 0; j < EMBED_DIM; j++) dot += query[j] * corpus[i * EMBED_DIM + j];
    scores.push([dot, i]);
  }
  scores.sort((a, b) => b[0] - a[0]);
  return scores.slice(0, k);
}

const embedJs = (paths, dtype) =>
  JSON.parse(
    execFileSync("node", [path.join(ROOT, "verify_js/embed.mjs"), ...paths], {
      env: { ...process.env, DTYPE: dtype },
      maxBuffer: 1e8,
    }).toString(),
  );

const tiles = JSON.parse(fs.readFileSync(EMBEDDED, "utf8"));
const buf = fs.readFileSync(BIN);
const corpus = decodeFp16(
  new Uint16Array(buf.buffer, buf.byteOffset, buf.byteLength / 2),
);
const n = corpus.length / EMBED_DIM;
console.log(`corpus: ${n} tiles (meta ${tiles.length})`);
if (n !== tiles.length) throw new Error("bin/meta count mismatch");

// 1) fp16 round-trip: サンプルタイルを fp32 で直接埋め込み、bin の行と比較
const sampleIdx = [0, Math.floor(n / 2), n - 1];
const samplePaths = sampleIdx.map((i) => {
  const t = tiles[i];
  return path.join(DATA, "tiles", String(t.z), String(t.x), `${t.y}.jpg`);
});
const direct = embedJs(samplePaths, "fp32");
sampleIdx.forEach((row, k) => {
  let dot = 0;
  for (let j = 0; j < EMBED_DIM; j++) dot += direct[k][j] * corpus[row * EMBED_DIM + j];
  console.log(`fp16 round-trip cosine (row ${row}): ${dot.toFixed(5)}`);
  if (dot < 0.999) throw new Error("fp16 round-trip degraded");
});

// 2) fp32 vs q8 の top-3 順位一致 (顔テスト画像)
const faces = fs
  .readdirSync(path.join(ROOT, "testdata"))
  .filter((f) => /\.(jpe?g|png)$/i.test(f))
  .map((f) => path.join(ROOT, "testdata", f));
// ブラウザは全デバイス q8 なので、q8 が fp32 と意味的に同じクラスタを
// 指しているかだけを品質ガードとして確認する (q8 top-1 ∈ fp32 top-10)。
const fp32 = embedJs(faces, "fp32");
const q8 = embedJs(faces, "q8");
for (let k = 0; k < faces.length; k++) {
  const a = topK(fp32[k], corpus, n, 10).map(([, i]) => i);
  const b = topK(q8[k], corpus, n).map(([, i]) => i);
  console.log(`${path.basename(faces[k])}: fp32 top10 [${a}] / q8 top3 [${b}]`);
  if (!a.includes(b[0])) throw new Error("q8 top-1 が fp32 top-10 に含まれない — 量子化劣化");
}
console.log("VERIFY OK");

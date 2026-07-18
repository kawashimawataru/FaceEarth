// tiles_filtered.json のタイルを Transformers.js (fp32, CPU) で埋め込み、
// fp16 バイナリを web/public/data/embeddings.bin に書く。
//
// Python ではなく Node で埋め込む理由: ブラウザ側 (clipWorker.ts) と
// 完全に同一のモデル・前処理・実装になり、埋め込みパリティの問題が消える。
// 依存は web/node_modules を利用する。
//
// 実行: node 04_embed_tiles.mjs

import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import fs from "node:fs";
import path from "node:path";

const ROOT = import.meta.dirname;
const webDir = path.resolve(ROOT, "../web");
const require = createRequire(path.join(webDir, "package.json"));
const { AutoProcessor, CLIPVisionModelWithProjection, RawImage } = await import(
  pathToFileURL(require.resolve("@huggingface/transformers")).href
);

const MODEL_ID = "Xenova/clip-vit-base-patch32"; // web/src/lib/config.ts と対
const EMBED_DIM = 512;
const DATA = path.join(ROOT, "data");
const FILTERED = path.join(DATA, "tiles_filtered.json");
const EMBEDDED = path.join(DATA, "tiles_embedded.json");
const OUT_BIN = path.resolve(ROOT, "../web/public/data/embeddings.bin");

const tilePath = (z, x, y) => path.join(DATA, "tiles", String(z), String(x), `${y}.jpg`);

/** fp32 → IEEE754 half (fp16)。matcher.ts の decodeFp16 と対。 */
function toFp16(f32) {
  const out = new Uint16Array(f32.length);
  const buf = new DataView(new ArrayBuffer(4));
  for (let i = 0; i < f32.length; i++) {
    buf.setFloat32(0, f32[i]);
    const x = buf.getUint32(0);
    const sign = (x >>> 16) & 0x8000;
    let exp = ((x >>> 23) & 0xff) - 127 + 15;
    let frac = (x >>> 13) & 0x3ff;
    if (exp <= 0) {
      // 非正規化数 (このデータでは実質発生しない)
      out[i] = sign;
    } else if (exp >= 0x1f) {
      out[i] = sign | 0x7c00;
    } else {
      // 丸め (round-to-nearest)
      if ((x >>> 12) & 1) frac += 1;
      out[i] = sign | (exp << 10) | (frac & 0x3ff);
    }
  }
  return out;
}

const processor = await AutoProcessor.from_pretrained(MODEL_ID);
const model = await CLIPVisionModelWithProjection.from_pretrained(MODEL_ID, {
  device: "cpu",
  dtype: "fp32",
});

const tiles = JSON.parse(fs.readFileSync(FILTERED, "utf8"));
const embedded = [];
const rows = [];
const t0 = Date.now();

for (const t of tiles) {
  const file = tilePath(t.z, t.x, t.y);
  if (!fs.existsSync(file)) continue;
  let image;
  try {
    image = await RawImage.read(file);
  } catch {
    continue;
  }
  const inputs = await processor(image);
  const { image_embeds } = await model(inputs);
  const v = Float32Array.from(image_embeds.data);
  let norm = 0;
  for (const x of v) norm += x * x;
  norm = Math.sqrt(norm) || 1;
  for (let i = 0; i < v.length; i++) v[i] /= norm;
  rows.push(v);
  embedded.push(t);
  if (embedded.length % 100 === 0) {
    const rate = embedded.length / ((Date.now() - t0) / 1000);
    console.log(`embedded ${embedded.length}/${tiles.length} (${rate.toFixed(1)}/s)`);
  }
}

const flat = new Float32Array(embedded.length * EMBED_DIM);
rows.forEach((v, i) => flat.set(v, i * EMBED_DIM));
const half = toFp16(flat);
fs.mkdirSync(path.dirname(OUT_BIN), { recursive: true });
fs.writeFileSync(OUT_BIN, Buffer.from(half.buffer));
fs.writeFileSync(EMBEDDED, JSON.stringify(embedded));
console.log(
  `wrote ${OUT_BIN} (${embedded.length} x ${EMBED_DIM}, ${(half.byteLength / 1e6).toFixed(1)} MB)`,
);

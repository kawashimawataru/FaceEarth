// Node で Transformers.js (Xenova/clip-vit-base-patch32) を使い、
// 引数の画像を埋め込んで JSON (N×512, L2 正規化済み) を stdout に出す。
// ブラウザ側 clipWorker.ts と同じモデル ID・前処理・正規化。
// 依存は web/node_modules を利用する。

import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";

const webDir = path.resolve(import.meta.dirname, "../../web");
const require = createRequire(path.join(webDir, "package.json"));
const pkgPath = require.resolve("@huggingface/transformers");
const { AutoProcessor, CLIPVisionModelWithProjection, RawImage } = await import(
  pathToFileURL(pkgPath).href
);

const MODEL_ID = "Xenova/clip-vit-base-patch32";

const processor = await AutoProcessor.from_pretrained(MODEL_ID);
const model = await CLIPVisionModelWithProjection.from_pretrained(MODEL_ID, {
  device: "cpu",
  dtype: process.env.DTYPE || "fp32",
});

const out = [];
for (const file of process.argv.slice(2)) {
  const image = await RawImage.read(file);
  const inputs = await processor(image);
  const { image_embeds } = await model(inputs);
  const v = Array.from(image_embeds.data);
  const norm = Math.sqrt(v.reduce((s, x) => s + x * x, 0)) || 1;
  out.push(v.map((x) => x / norm));
}
process.stdout.write(JSON.stringify(out));

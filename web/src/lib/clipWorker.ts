/**
 * Web Worker: CLIP ビジョンモデルの読み込みと画像埋め込み。
 * モデル DL(~90MB)と推論を main thread から隔離する。
 *
 * 受信: { type: "load" } | { type: "embed", id, bitmap }
 * 送信: { type: "progress", file, progress } | { type: "ready", device }
 *      | { type: "embedding", id, vector } | { type: "error", id?, message }
 */

import {
  AutoProcessor,
  CLIPVisionModelWithProjection,
  RawImage,
  type ProgressInfo,
} from "@huggingface/transformers";
import { MODEL_ID } from "./config";

// Worker コンテキストの postMessage (DOM の window 版と型が違うため)
const post = self.postMessage.bind(self) as (msg: unknown, transfer?: Transferable[]) => void;

type Processor = Awaited<ReturnType<typeof AutoProcessor.from_pretrained>>;

let model: CLIPVisionModelWithProjection | null = null;
let processor: Processor | null = null;
let loading: Promise<string> | null = null;

async function hasWebGPU(): Promise<boolean> {
  const gpu = (navigator as { gpu?: { requestAdapter(): Promise<unknown> } }).gpu;
  if (!gpu) return false;
  try {
    return (await gpu.requestAdapter()) != null;
  } catch {
    return false;
  }
}

function load(): Promise<string> {
  loading ??= (async () => {
    const webgpu = await hasWebGPU();
    const device = webgpu ? "webgpu" : "wasm";
    const dtype = webgpu ? "fp16" : "q8";
    const progress_callback = (info: ProgressInfo) => {
      if (info.status === "progress") {
        post({ type: "progress", file: info.file, progress: info.progress });
      }
    };
    processor = await AutoProcessor.from_pretrained(MODEL_ID, { progress_callback });
    model = await CLIPVisionModelWithProjection.from_pretrained(MODEL_ID, {
      device,
      dtype,
      progress_callback,
    });
    return device;
  })();
  return loading;
}

async function embed(bitmap: ImageBitmap): Promise<Float32Array> {
  await load();
  const canvas = new OffscreenCanvas(bitmap.width, bitmap.height);
  const ctx = canvas.getContext("2d")!;
  ctx.drawImage(bitmap, 0, 0);
  const { data, width, height } = ctx.getImageData(0, 0, bitmap.width, bitmap.height);
  const image = new RawImage(new Uint8ClampedArray(data), width, height, 4).rgb();

  const inputs = await processor!(image);
  const output = await model!(inputs);
  const embeds = output.image_embeds.data as Float32Array;

  // L2 正規化 — コーパス側も正規化済み(pipeline/04_embed_tiles.py)
  let norm = 0;
  for (let i = 0; i < embeds.length; i++) norm += embeds[i] * embeds[i];
  norm = Math.sqrt(norm) || 1;
  const out = new Float32Array(embeds.length);
  for (let i = 0; i < embeds.length; i++) out[i] = embeds[i] / norm;
  return out;
}

self.onmessage = async (e: MessageEvent) => {
  const msg = e.data;
  try {
    if (msg.type === "load") {
      const device = await load();
      post({ type: "ready", device });
    } else if (msg.type === "embed") {
      const vector = await embed(msg.bitmap);
      post({ type: "embedding", id: msg.id, vector }, [vector.buffer]);
    }
  } catch (err) {
    post({
      type: "error",
      id: msg.id,
      message: err instanceof Error ? err.message : String(err),
    });
  }
};

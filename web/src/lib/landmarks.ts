/** MediaPipe FaceLandmarker のラッパー。478 点の顔ランドマークをピクセル座標で返す。 */

import { FaceLandmarker, FilesetResolver } from "@mediapipe/tasks-vision";
import { FACE_LANDMARKER_URL } from "./config";

let landmarkerPromise: Promise<FaceLandmarker> | null = null;

function getLandmarker(): Promise<FaceLandmarker> {
  landmarkerPromise ??= (async () => {
    const fileset = await FilesetResolver.forVisionTasks(
      `${import.meta.env.BASE_URL}mediapipe-wasm`,
    );
    return FaceLandmarker.createFromOptions(fileset, {
      baseOptions: { modelAssetPath: FACE_LANDMARKER_URL },
      runningMode: "IMAGE",
      numFaces: 1,
    });
  })();
  return landmarkerPromise;
}

export interface FaceLandmarks {
  /** ピクセル座標 (入力画像スケール) の 478 点 */
  points: Array<{ x: number; y: number }>;
}

/** 顔が見つからなければ null (旧実装のような偽のフォールバックはしない) */
export async function detectFace(image: ImageBitmap): Promise<FaceLandmarks | null> {
  const landmarker = await getLandmarker();
  const result = landmarker.detect(image);
  const face = result.faceLandmarks[0];
  if (!face) return null;
  return {
    points: face.map((p) => ({ x: p.x * image.width, y: p.y * image.height })),
  };
}

/** 顔の輪郭 (face oval) を構成するランドマーク番号列 (MediaPipe 標準の接続順) */
export const FACE_OVAL_INDICES = [
  10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378,
  400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21,
  54, 103, 67, 109, 10,
];

/**
 * アプリ全体の定数。
 * MODEL_ID と EMBED_DIM は pipeline/config.py と対になっている(データ契約)。
 * 変更するときは必ず両方を揃え、pipeline を再実行すること。
 */

/** ブラウザ側 CLIP モデル (Python 側は openai/clip-vit-base-patch32 と同一重み) */
export const MODEL_ID = "Xenova/clip-vit-base-patch32";

/** CLIP ViT-B/32 の射影後の埋め込み次元 */
export const EMBED_DIM = 512;

/** 事前計算した衛星タイル埋め込み (fp16, N×EMBED_DIM) */
export const EMBEDDINGS_URL = `${import.meta.env.BASE_URL}data/embeddings.bin`;

/** タイルのメタデータ (緯度経度・地域名・traits) */
export const TILES_META_URL = `${import.meta.env.BASE_URL}data/tiles.meta.json`;

/** MediaPipe FaceLandmarker モデル (セルフホスト) */
export const FACE_LANDMARKER_URL = `${import.meta.env.BASE_URL}models/face_landmarker.task`;

/**
 * EOX Sentinel-2 Cloudless 2016 (CC-BY 4.0)。
 * pipeline/config.py の TILE_URL_TEMPLATE と同一であること —
 * 埋め込んだ画像と画面に見せる画像を一致させる。
 */
export const TILE_URL_TEMPLATE =
  "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2016_3857/default/GoogleMapsCompatible/{z}/{y}/{x}.jpg";

export const TILE_ATTRIBUTION =
  '<a href="https://s2maps.eu">Sentinel-2 cloudless</a> by <a href="https://eox.at">EOX IT Services GmbH</a> (CC BY 4.0)';

/** マッチ結果として表示する候補数 */
export const TOP_K = 3;

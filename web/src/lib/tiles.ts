/** Web Mercator (EPSG:3857) のタイル座標まわりの数学 */

import { TILE_URL_TEMPLATE } from "./config";

export interface TileMeta {
  /** embeddings.bin 内の行番号 */
  i: number;
  z: number;
  x: number;
  y: number;
  /** タイル中心の緯度経度 */
  lat: number;
  lng: number;
  /** 国名 (日本語優先) */
  country: string;
  /** 地域名 (州・県レベル、無ければ空) */
  region: string;
  /** 地形の特徴タグ: desert / forest / mountain / coast / ice / plain ... */
  traits: string[];
}

export function tileUrl(z: number, x: number, y: number): string {
  return TILE_URL_TEMPLATE.replace("{z}", String(z))
    .replace("{x}", String(x))
    .replace("{y}", String(y));
}

/** タイル左上角の経度 */
export function tile2lng(x: number, z: number): number {
  return (x / 2 ** z) * 360 - 180;
}

/** タイル左上角の緯度 */
export function tile2lat(y: number, z: number): number {
  const n = Math.PI - (2 * Math.PI * y) / 2 ** z;
  return (180 / Math.PI) * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n)));
}

/** タイル中心の緯度経度 */
export function tileCenter(z: number, x: number, y: number): { lat: number; lng: number } {
  return {
    lat: (tile2lat(y, z) + tile2lat(y + 1, z)) / 2,
    lng: (tile2lng(x, z) + tile2lng(x + 1, z)) / 2,
  };
}

/** 度 → 度分秒表記 (結果画面の計測データ表示用) */
export function formatDMS(lat: number, lng: number): string {
  const dms = (v: number) => {
    const a = Math.abs(v);
    const d = Math.floor(a);
    const m = Math.floor((a - d) * 60);
    const s = ((a - d) * 60 - m) * 60;
    return `${d}°${String(m).padStart(2, "0")}′${s.toFixed(1).padStart(4, "0")}″`;
  };
  const ns = lat >= 0 ? "N" : "S";
  const ew = lng >= 0 ? "E" : "W";
  return `${dms(lat)}${ns} ${dms(lng)}${ew}`;
}

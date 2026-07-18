/**
 * 占い風テキストの生成。
 * (タイル ID, 共鳴度) から決定的にシードし、同じ顔×同じ場所なら常に同じ文になる。
 * 土地の traits と地名を織り込んだテンプレートバンクから組み立てる。
 */

import { seededRandom } from "./correspondence";
import type { MatchResult } from "./matcher";
import { formatDMS } from "./tiles";

const TRAIT_READINGS: Record<string, string[]> = {
  desert: [
    "乾いた大地は、余計なものを削ぎ落として生きる強さの相です",
    "砂の紋様は、風に流されてもまた形を結ぶ、しなやかな心を映しています",
    "昼と夜の寒暖を受け止める砂漠は、感情の振れ幅をそのまま抱きしめる度量の証です",
  ],
  forest: [
    "深い緑は、静かに人を癒す包容力の相です",
    "森の天蓋は、見えないところで無数の命を支える縁の下の力を表します",
    "湿った土と木々の呼吸は、時間をかけて物事を育てる粘り強さを映しています",
  ],
  mountain: [
    "刻まれた尾根は、困難を越えるたびに輪郭が際立つ人生の相です",
    "山肌の陰影は、光の当たり方で違う顔を見せる多面性の証です",
    "隆起した大地は、内に秘めた情熱が形になって現れる予兆です",
  ],
  coast: [
    "海と陸の境界線は、異なる世界をつなぐ橋渡しの才の相です",
    "打ち寄せる波に削られた海岸は、出会いと別れを重ねて磨かれる魂を映しています",
    "入り組んだ入江は、懐の深さと、たやすく本心を見せない奥ゆかしさの証です",
  ],
  ice: [
    "白く輝く氷雪は、澄んだ心と揺るがない意志の相です",
    "凍てつく大地の下で春を待つ力は、静かな忍耐の証です",
  ],
  plain: [
    "広がる平原は、どんなものも受け入れる寛容の相です",
    "遮るもののない大地は、遠くを見晴らす視野の広さを映しています",
  ],
};

const OPENINGS = [
  "地球をひと巡りした観測の末、あなたの顔は {place} の大地と最も強く響き合いました。",
  "{n} 枚の衛星画像の中から、あなたに似た土地が見つかりました。{place} です。",
  "座標 {coords}。あなたと同じ表情をした大地が、{place} にありました。",
];

const CLOSINGS = [
  "縁とは、似ていることから始まるのかもしれません。いつかこの座標を訪ねてみてください。",
  "遠く離れたこの土地は、今日からあなたの「もうひとつの故郷」です。",
  "地図でこの場所をなぞるとき、あなたは少しだけこの土地の住人になります。",
  "「似ている」と知ってしまった以上、この土地のニュースはもう他人事ではありません。",
];

export function tellFortune(m: MatchResult, corpusSize: number): string {
  const rng = seededRandom(m.meta.i * 7919 + Math.round(m.resonance * 100));
  const pick = <T,>(arr: T[]): T => arr[Math.floor(rng() * arr.length)];

  const place =
    m.meta.country && m.meta.region
      ? `${m.meta.country}・${m.meta.region}`
      : m.meta.country || "名もなき土地";

  const opening = pick(OPENINGS)
    .replace("{place}", place)
    .replace("{n}", corpusSize.toLocaleString())
    .replace("{coords}", formatDMS(m.meta.lat, m.meta.lng));

  const readings = m.meta.traits
    .map((t) => TRAIT_READINGS[t])
    .filter(Boolean)
    .map((bank) => pick(bank!));

  // 各文が「。」で終わるように整えて連結する
  return [opening, ...readings, pick(CLOSINGS)]
    .map((s) => (s.endsWith("。") ? s : `${s}。`))
    .join("");
}

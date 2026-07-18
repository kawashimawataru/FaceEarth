# FaceEarth

あなたの顔は、地球のどこかに似ている。

FaceEarth は、顔写真 1 枚から地球上の「あなたに似た土地」を探し出すメディアアートプロジェクトです。
AI が顔と地球全体の衛星画像を照合し、最も響き合う場所を特定。3D 地球儀でその土地へ飛び、
顔のランドマークと地形の対応点を線で結んだアートワークと、その土地との「縁」を語る占い風のテキストを生成します。

## Philosophy

> 「土地を愛しているのか、果たして自分たちは？」

「〜〜って〜〜に似てるよね」と言われると、なぜか親近感が湧く。
このプロジェクトは、**「共通点」こそが親近感を生み、興味や愛を育むきっかけになる**という仮説に基づいています。
AI によって強引にでも自分と土地の「類似性」を見出すことで、遠く離れた見知らぬ土地に親近感を抱き、
そこから土地への、ひいては地球全体への興味へと繋げていく。「占い」のような、あるいは「運命」のような体験です。
(2024年 ニューヨークにて発表 / 2026年 全面リビルド)

## 仕組み

すべての解析は**ブラウザの中だけ**で行われます。顔写真が端末の外に送信されることはありません。

```
[オフライン pipeline/]                       [ブラウザ web/]
EOX Sentinel-2 衛星タイル (z=7, 陸のみ)        顔写真
  → CLIP ViT-B/32 で埋め込み (512次元)          → Transformers.js (CLIP) で埋め込み
  → fp16 バイナリ + メタデータとして静的配信      → 約5,000タイルと総当たり cosine 照合
                                               → MapLibre の 3D 地球儀でその土地へ飛行
                                               → MediaPipe 顔ランドマーク × 地形の対応線アート
                                               → 土地の特徴から占い風テキストを生成
```

## 技術スタック

### Web (`/web`) — ブラウザ完結型 SPA

- **Vite + React + TypeScript**
- **Transformers.js** (`Xenova/clip-vit-base-patch32`): ブラウザ内 CLIP 推論 (WebGPU / WASM)
- **MediaPipe Tasks Vision**: 顔ランドマーク検出 (478 点)
- **MapLibre GL JS**: 3D 地球儀表示

### Pipeline (`/pipeline`) — 事前計算 (Python)

- 衛星タイルの収集 (EOX Sentinel-2 Cloudless 2016, 陸地のみ z=7)
- CLIP 埋め込みの事前計算 → `web/public/data/embeddings.bin`
- Natural Earth による逆ジオコーディングと地形特徴タグ付け

## 実行方法

### Web アプリ

```bash
cd web
npm install
npm run dev
```

### データパイプライン (データを作り直す場合のみ)

```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python 01_list_tiles.py && python 02_download_tiles.py && python 03_filter_tiles.py
python 04_embed_tiles.py && python 05_metadata.py
```

## クレジット

- 衛星画像: [Sentinel-2 cloudless](https://s2maps.eu) by [EOX IT Services GmbH](https://eox.at) (CC BY 4.0), 2016 データ
- 行政界・地名: [Natural Earth](https://www.naturalearthdata.com/) (Public Domain)

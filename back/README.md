# my-fastapi-app/my-fastapi-app/README.md

# my-fastapi-app

このプロジェクトは、FastAPIを使用して画像の類似度を分析するAPIを提供します。Googleマップから取得した画像と与えられた画像を比較し、最も類似度の高い画像を特定します。

## 構成ファイル

- `src/main.py`: アプリケーションのエントリーポイント。APIの設定とエンドポイントを提供します。
- `src/similarity.py`: 画像の類似度を計算するための関数やクラスを定義します。画像のリサイズ、回転、マッチング、Googleマップからの画像取得などの機能を実装します。
- `requirements.txt`: プロジェクトの依存関係をリストします。

## インストール手順

1. リポジトリをクローンします。
   ```
   git clone <repository-url>
   cd my-fastapi-app
   ```

2. 必要なパッケージをインストールします。
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. アプリケーションを起動します。
   ```
   uvicorn src.main:app --reload
   ```

2. ブラウザまたはAPIクライアントを使用して、以下のエンドポイントにアクセスします。
   - `GET /`: "Hello World!" メッセージを返します。
   - `GET /analyze`: 画像の類似度を分析し、結果を返します。

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。
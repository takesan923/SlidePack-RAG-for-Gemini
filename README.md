# SlidePack-RAG-for-Gemini

簡易的な**RAG**システム。SlidePack のドキュメントをベクトル化し、Vertex AIで回答を生成

## 主な機能
- Markdown ドキュメントの分割（見出し単位）→埋め込み→PGVector（Postgres+pgvector）へ格納
- LangChain を使った Retriever + Vertex AI（Gemini）による生成
- WEBブラウザ上対話型チャット

## 前提条件
- Python 3.10+
- Docker / Docker Desktop（pgvector コンテナ用）
- Google Cloud Account
- 仮想環境推奨（.venv）

## セットアップ（簡易）
1. 仮想環境作成・有効化（bash）
```bash
python -m venv .venv
source ./.venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
```
2. .env を作成（必要なキー）
```
GOOGLE_APPLICATION_CREDENTIALS=./.Secret/your-key.json
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-project-location
```
3. Docker（pgvector）起動
```bash
docker compose up -d
```

## 実行
- ドキュメントをベクトル化して保存（index スクリプト）
```bash
python ./App/index.py
```
- ターミナルチャット（対話式）
```bash
python ./App/main.py
```

## よくあるエラー
- 認証エラー: Application Default Credentials が未設定 →GoogleCloudでサービスアカウントを作成し認証用JSON を `.env` の `GOOGLE_APPLICATION_CREDENTIALS` に設定
- モデルが見つからない: 指定リージョンで利用可能なモデル名を確認し`GOOGLE_CLOUD_LOCATION` を変更
- pgvector 接続エラー: Docker Desktop 起動、ポート（6024）が空いているか確認、拡張 `vector` が有効かチェック

## 諸注意
- 機密情報は `.Secret/` と `.env` に置き、`.gitignore` に含めること

## Frontend

### 主な技術
- TypeScript
- React
- Vite

### セットアップ
1. 必要なパッケージをインストール
```bash
cd Frontend
npm install
```

2. 開発サーバーを起動
```bash
npm run dev
```

3. ビルド
```bash
npm run build
```

### 構成
- `src/` : 主なソースコード
  - `main.tsx` : エントリーポイント
  - `Chat.tsx` : チャットコンポーネント
- `public/` : 公開用静的ファイル

### 注意点
- ESLint と Prettier を使用してコード品質を維持
- `vite.config.ts` でプロジェクト設定を管理
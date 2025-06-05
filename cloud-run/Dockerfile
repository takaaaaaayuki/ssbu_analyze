FROM python:3.9-slim
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存関係を先にコピーしてキャッシュを効率化
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# imagesディレクトリを作成
RUN mkdir -p images

# ポート8080を公開
EXPOSE 8080

# 環境変数の定義
ENV PORT=8080

# アプリケーションの実行
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
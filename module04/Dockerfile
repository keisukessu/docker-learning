# Python 3.12 の軽量版をベースに使う
FROM python:3.12-slim

# 作業ディレクトリを /app に設定
WORKDIR /app

# 依存ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY app.py .

# ポート 8080 を公開
EXPOSE 8080

# アプリを起動
CMD ["python", "app.py"]

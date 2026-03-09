# Module 6: Docker Compose

## 目標
- docker-compose.yml の書き方を理解する
- 複数コンテナを一括管理できる
- Web アプリ + DB の開発環境を構築する

---

## Docker Compose とは

複数のコンテナをまとめて管理するツールです。

**コマンド一発で全部起動できる！**

```bash
# 全サービスを起動
docker compose up -d

# 全サービスを停止・削除
docker compose down
```

---

## docker-compose.yml の基本構造

```yaml
services:
  サービス名1:
    image: イメージ名
    ports:
      - "ホストポート:コンテナポート"
    environment:
      - 環境変数=値
    volumes:
      - ボリューム名:/コンテナのパス

  サービス名2:
    build: .        # Dockerfile からビルド
    depends_on:
      - サービス名1  # サービス名1 が起動してから起動する

volumes:
  ボリューム名:      # ボリュームの定義
```

---

## ハンズオン: Flask + PostgreSQL の開発環境

### プロジェクト構成

```
module06/
├── docker-compose.yml
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── .env
```

### .env ファイル（環境変数の管理）

```env
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
```

### app/requirements.txt

```
flask==3.0.0
psycopg2-binary==2.9.9
```

### app/app.py

```python
import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('POSTGRES_DB', 'mydb'),
        user=os.environ.get('POSTGRES_USER', 'myuser'),
        password=os.environ.get('POSTGRES_PASSWORD', 'mypassword'),
    )
    return conn

@app.route('/')
def index():
    return '<h1>Flask + PostgreSQL on Docker!</h1>'

@app.route('/health')
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({'status': 'ok', 'db': 'connected'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### app/Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### docker-compose.yml

```yaml
services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - DB_HOST=db
    depends_on:
      - db
    volumes:
      - ./app:/app   # 開発時にコードの変更を即反映

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres-data:
```

---

## Docker Compose コマンド

```bash
# 全サービスをビルドして起動（バックグラウンド）
docker compose up -d --build

# 起動中のサービスを確認
docker compose ps

# ログを見る
docker compose logs

# 特定サービスのログをリアルタイムで追う
docker compose logs -f web

# サービスに入る
docker compose exec web bash
docker compose exec db psql -U myuser -d mydb

# 全サービスを停止（コンテナとネットワークを削除、ボリュームは残る）
docker compose down

# ボリュームも含めて全部削除
docker compose down -v
```

---

## 実行手順

### ステップ 1: ファイルを作成

上記のファイル構成で各ファイルを作成してください。

### ステップ 2: 起動

```bash
cd module06
docker compose up -d --build
```

### ステップ 3: 確認

```bash
# サービスの状態を確認
docker compose ps

# ブラウザでアクセス
# http://localhost:5000        ← Flask アプリ
# http://localhost:5000/health ← DB 接続確認
```

### ステップ 4: データベースに接続

```bash
docker compose exec db psql -U myuser -d mydb

# PostgreSQL のプロンプト
\l          # データベース一覧
\dt         # テーブル一覧
\q          # 終了
```

### ステップ 5: 後片付け

```bash
docker compose down -v
```

---

## チェックリスト

- [ ] docker-compose.yml が書けた
- [ ] `docker compose up -d` で全サービスが起動した
- [ ] ブラウザで Flask アプリが確認できた
- [ ] `/health` エンドポイントで DB 接続が確認できた
- [ ] `docker compose down` で全サービスが停止できた

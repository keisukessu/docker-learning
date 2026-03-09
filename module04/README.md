# Module 4: Dockerfile でイメージを作る

## 目標
- Dockerfile の基本命令を理解する
- 自分でイメージをビルドできる
- シンプルな Web アプリをコンテナ化する

---

## Dockerfile とは

Dockerfile は **イメージの作り方を書いたテキストファイル** です。

```
Dockerfile（レシピ）→ docker build → Image（完成品）→ docker run → Container（動いているもの）
```

---

## Dockerfile の基本命令

```dockerfile
# ベースイメージを指定（必須・最初に書く）
FROM python:3.12-slim

# 作業ディレクトリを設定（以降のコマンドはここで実行される）
WORKDIR /app

# ファイルをコンテナにコピー
COPY . .

# コマンドを実行（パッケージインストールなど）
RUN pip install -r requirements.txt

# ポートを公開（ドキュメント的な意味。-p オプションと組み合わせて使う）
EXPOSE 8000

# コンテナ起動時に実行するコマンド
CMD ["python", "app.py"]
```

### 命令の詳細

| 命令 | 意味 |
|------|------|
| `FROM` | ベースイメージを指定。Dockerfile の最初に必ず書く |
| `WORKDIR` | 作業ディレクトリを設定。存在しなければ自動作成 |
| `COPY` | ホストのファイルをイメージにコピー |
| `RUN` | ビルド時にコマンドを実行（パッケージインストールなど） |
| `EXPOSE` | コンテナが使うポートを宣言（実際の公開は `-p` で行う） |
| `CMD` | コンテナ起動時に実行するデフォルトコマンド |
| `ENV` | 環境変数を設定 |

---

## ハンズオン: Python Web アプリをコンテナ化

### プロジェクト構成

```
module04/
├── Dockerfile
├── requirements.txt
└── app.py
```

### app.py

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <html>
        <body>
            <h1>Hello from Docker!</h1>
            <p>Python Web サーバーがコンテナ内で動いています。</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[アクセス] {args[0]} {args[1]}")

if __name__ == '__main__':
    print("サーバーを起動します: http://localhost:8080")
    server = HTTPServer(('0.0.0.0', 8080), HelloHandler)
    server.serve_forever()
```

### requirements.txt

（このアプリは標準ライブラリのみ使うので空でOK）

```
# 依存パッケージなし
```

### Dockerfile

```dockerfile
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
```

---

## ビルドと実行

### ステップ 1: イメージをビルド

```bash
# module04 ディレクトリに移動
cd module04

# イメージをビルド（. は Dockerfile のある場所）
docker build -t my-python-app .
```

**オプション:**
- `-t my-python-app`: イメージに名前（タグ）をつける
- `.`: Dockerfile がある場所（現在のディレクトリ）

**ビルドの流れ（出力例）:**
```
[+] Building 15.2s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/4] FROM python:3.12-slim
 => [2/4] WORKDIR /app
 => [3/4] COPY requirements.txt .
 => [4/4] RUN pip install --no-cache-dir -r requirements.txt
 => COPY app.py .
 => exporting to image
```

### ステップ 2: イメージを確認

```bash
docker images
```

`my-python-app` が一覧に表示されるはず。

### ステップ 3: コンテナを起動

```bash
docker run -d --name myapp -p 8080:8080 my-python-app
```

### ステップ 4: ブラウザで確認

```
http://localhost:8080
```

**"Hello from Docker!" が表示されれば成功！**

### ステップ 5: 後片付け

```bash
docker stop myapp
docker rm myapp
docker rmi my-python-app
```

---

## .dockerignore ファイル

`.dockerignore` に書いたファイルは `COPY` でコピーされません。
（Git の `.gitignore` と同じ仕組み）

```
# .dockerignore の例
__pycache__/
*.pyc
.git/
.env
node_modules/
```

---

## チェックリスト

- [ ] Dockerfile の各命令の意味が理解できた
- [ ] `docker build -t my-python-app .` でビルドできた
- [ ] `docker images` で自作イメージが確認できた
- [ ] ブラウザで "Hello from Docker!" が表示できた
- [ ] `docker stop` → `docker rm` → `docker rmi` で後片付けできた

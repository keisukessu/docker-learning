# Module 3: イメージの理解

## 目標
- Docker Hub でイメージを探せるようになる
- イメージの管理コマンドをマスターする
- Nginx を起動してブラウザで確認する

---

## Docker Hub とは

**Docker Hub** は Docker 公式のイメージレジストリ（保管庫）です。
URL: https://hub.docker.com

```
Docker Hub にあるイメージの例:
- ubuntu     ← Ubuntu OS
- nginx      ← Web サーバー
- python     ← Python 環境
- node       ← Node.js 環境
- mysql      ← MySQL データベース
- postgres   ← PostgreSQL データベース
- redis      ← Redis キャッシュサーバー
```

### 公式イメージ vs コミュニティイメージ

- **公式イメージ**: Docker 社または開発元が管理。安全で信頼できる。
  - 例: `nginx`, `python`, `mysql`
- **コミュニティイメージ**: 個人・企業が公開。`username/imagename` の形式。
  - 例: `mycompany/myapp`

---

## イメージの基本コマンド

### イメージをダウンロードする

```bash
docker pull <イメージ名>

# バージョン（タグ）を指定する
docker pull nginx:1.25
docker pull python:3.12
docker pull ubuntu:22.04
```

### ダウンロード済みのイメージを一覧表示

```bash
docker images
```

**出力例:**
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    a6bd71f48f68   2 weeks ago    187MB
ubuntu       latest    bf3dc08bfed0   3 weeks ago    77.9MB
```

### イメージを削除する

```bash
docker rmi <イメージ名またはID>

# 使っていないイメージをまとめて削除
docker image prune
```

---

## イメージのタグについて

```bash
docker pull nginx        # latest タグ（最新版）
docker pull nginx:latest # 同じ意味
docker pull nginx:1.25   # バージョン 1.25
docker pull nginx:alpine # Alpine Linux ベース（軽量版）
```

**本番環境では必ずバージョンを固定する！**
（`latest` は更新されて動かなくなることがある）

---

## ハンズオン: Nginx を起動してブラウザで確認しよう

### ステップ 1: Nginx イメージを取得

```bash
docker pull nginx
```

### ステップ 2: Nginx コンテナを起動（ポートマッピング）

```bash
docker run -d --name mynginx -p 8080:80 nginx
```

**ポートマッピングの意味:**
```
-p 8080:80
    │    └── コンテナ内のポート（Nginx が使っている）
    └─────── ホスト（あなたのPC）のポート（ブラウザでアクセスするポート）
```

### ステップ 3: ブラウザで確認

ブラウザを開いて以下の URL にアクセス:
```
http://localhost:8080
```

**"Welcome to nginx!" のページが表示されれば成功！**

### ステップ 4: コンテナの状態を確認

```bash
docker ps
```

STATUS が `Up` になっているはず。

### ステップ 5: Nginx のログを見る

```bash
docker logs mynginx

# ブラウザで更新してからもう一度見る（アクセスログが追加される）
docker logs -f mynginx
# Ctrl+C で終了
```

### ステップ 6: コンテナを停止・削除

```bash
docker stop mynginx
docker rm mynginx
```

---

## イメージの情報を調べる

```bash
# イメージの詳細情報
docker inspect nginx

# イメージのレイヤー構造を見る
docker history nginx
```

---

## よく使うイメージのタグ一覧

| イメージ | タグ例 | 用途 |
|---------|--------|------|
| ubuntu | `22.04`, `20.04` | Ubuntu OS |
| nginx | `1.25`, `alpine` | Web サーバー |
| python | `3.12`, `3.12-slim` | Python |
| node | `20`, `20-alpine` | Node.js |
| mysql | `8.0`, `5.7` | MySQL |
| postgres | `16`, `15-alpine` | PostgreSQL |

---

## チェックリスト

- [ ] `docker pull nginx` でイメージをダウンロードできた
- [ ] `docker images` でイメージ一覧が確認できた
- [ ] `-p 8080:80` の意味が理解できた
- [ ] ブラウザで `http://localhost:8080` にアクセスできた
- [ ] `docker stop` と `docker rm` でコンテナを後片付けできた

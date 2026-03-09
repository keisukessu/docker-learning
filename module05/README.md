# Module 5: データの永続化

## 目標
- コンテナ削除でデータが消える問題を体験する
- ボリュームとバインドマウントの違いを理解する
- データが消えない MySQL コンテナを作る

---

## 問題: コンテナを削除するとデータが消える

```bash
# Ubuntu コンテナでファイルを作成
docker run -it --name test ubuntu bash

# コンテナ内でファイルを作る
echo "大切なデータ" > /tmp/important.txt
cat /tmp/important.txt
exit

# コンテナを削除
docker rm test

# 同じイメージで新しいコンテナを作っても...
docker run -it --name test2 ubuntu bash
cat /tmp/important.txt  # エラー！ファイルが消えている
exit
docker rm test2
```

コンテナはステートレス（状態を持たない）が基本。
データを残すには **ボリューム** か **バインドマウント** を使う。

---

## 解決策 1: ボリューム（Volumes）

Docker が管理する専用の保存領域。
Docker が管理する場所（`/var/lib/docker/volumes/`）に保存される。

```
あなたのPC
├── Docker の管理エリア
│   └── volumes/
│       └── mydata/      ← Docker が管理するボリューム
└── コンテナ
    └── /data/ ←→ mydata をマウント（共有）
```

### ボリュームのコマンド

```bash
# ボリュームを作成
docker volume create mydata

# ボリューム一覧を表示
docker volume ls

# ボリュームの詳細情報
docker volume inspect mydata

# ボリュームを削除
docker volume rm mydata

# 使っていないボリュームを全削除
docker volume prune
```

### ボリュームを使ってコンテナを起動

```bash
docker run -it --name test -v mydata:/data ubuntu bash

# コンテナ内でファイルを作成
echo "永続化データ" > /data/important.txt
exit

# コンテナを削除
docker rm test

# 新しいコンテナで同じボリュームをマウント
docker run -it --name test2 -v mydata:/data ubuntu bash
cat /data/important.txt  # データが残っている！
exit
docker rm test2
```

---

## 解決策 2: バインドマウント（Bind Mounts）

ホスト（あなたのPC）の特定のフォルダをコンテナにマウントする。

```
あなたのPC
├── C:/Users/keisu/myproject/  ← ホストのフォルダ
└── コンテナ
    └── /app/ ←→ C:/Users/keisu/myproject/ をマウント
```

### バインドマウントを使ってコンテナを起動

```bash
# Windows の場合（パスの形式に注意）
docker run -it -v "C:/Users/keisu/OneDrive - 学校法人立命館/docker-learning/module05/data":/data ubuntu bash

# コンテナ内でファイルを作成
echo "ホストにも保存される" > /data/test.txt
exit
```

ホストの `module05/data/` フォルダに `test.txt` が作られているはず！

---

## ボリュームとバインドマウントの比較

| 項目 | ボリューム | バインドマウント |
|------|-----------|----------------|
| 管理 | Docker が管理 | ユーザーが指定 |
| 場所 | Docker 管理エリア | ホストの任意の場所 |
| 用途 | DB データの永続化 | 開発時のコード共有 |
| 移植性 | 高い | 低い（パスが固定される） |
| 推奨 | 本番環境 | 開発環境 |

---

## ハンズオン: データが消えない MySQL コンテナ

### ステップ 1: ボリュームを作成

```bash
docker volume create mysql-data
```

### ステップ 2: MySQL コンテナを起動

```bash
docker run -d \
  --name mymysql \
  -e MYSQL_ROOT_PASSWORD=mypassword \
  -e MYSQL_DATABASE=testdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0
```

**環境変数の説明:**
- `MYSQL_ROOT_PASSWORD`: root ユーザーのパスワード
- `MYSQL_DATABASE`: 起動時に作成するデータベース名

### ステップ 3: MySQL に接続してデータを作成

```bash
# MySQL コンテナに入る
docker exec -it mymysql mysql -u root -pmypassword

# データベースを選択
USE testdb;

# テーブルを作成
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100)
);

# データを挿入
INSERT INTO users (name) VALUES ('山田太郎');
INSERT INTO users (name) VALUES ('鈴木花子');

# 確認
SELECT * FROM users;

# MySQL を終了
exit
```

### ステップ 4: コンテナを削除して再作成

```bash
# コンテナを停止・削除
docker stop mymysql
docker rm mymysql

# 同じボリュームで新しいコンテナを起動
docker run -d \
  --name mymysql2 \
  -e MYSQL_ROOT_PASSWORD=mypassword \
  -e MYSQL_DATABASE=testdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0

# データが残っているか確認
docker exec -it mymysql2 mysql -u root -pmypassword -e "SELECT * FROM testdb.users;"
```

データが残っていれば成功！

### ステップ 5: 後片付け

```bash
docker stop mymysql2
docker rm mymysql2
docker volume rm mysql-data
```

---

## チェックリスト

- [ ] コンテナ削除でデータが消えることを体験した
- [ ] `docker volume create` でボリュームを作れた
- [ ] `-v` オプションでボリュームをマウントできた
- [ ] コンテナ削除後もデータが残ることを確認した
- [ ] バインドマウントとボリュームの違いが説明できる

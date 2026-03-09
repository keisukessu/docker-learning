# Module 2: コンテナの基本操作

## 目標
- コンテナのライフサイクルを理解する
- 基本コマンドをマスターする
- Ubuntu コンテナに入って操作できる

---

## コンテナのライフサイクル

```
           docker run
  なし ──────────────→ 作成＆起動
                           │
                    docker stop
                           │
                           ↓
                         停止中
                           │
                    docker start
                           │
                           ↓
                          起動中
                           │
                    docker rm
                           │
                           ↓
                         削除
```

---

## 基本コマンド一覧

### コンテナを起動する

```bash
docker run <イメージ名>
```

よく使うオプション：

| オプション | 意味 | 例 |
|-----------|------|-----|
| `-d` | バックグラウンドで起動 | `docker run -d nginx` |
| `-it` | インタラクティブモード | `docker run -it ubuntu` |
| `--name` | コンテナに名前をつける | `docker run --name myapp nginx` |
| `-p` | ポートをマッピング | `docker run -p 8080:80 nginx` |
| `--rm` | 停止したら自動削除 | `docker run --rm ubuntu echo hello` |

### コンテナの一覧を見る

```bash
# 起動中のコンテナだけ表示
docker ps

# 停止中も含めて全部表示
docker ps -a
```

**出力例:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED         STATUS    PORTS     NAMES
a1b2c3d4e5f6   ubuntu    "bash"    2 minutes ago   Up 2 min            myubuntu
```

### コンテナを停止する

```bash
docker stop <コンテナID または 名前>
```

### コンテナを削除する

```bash
docker rm <コンテナID または 名前>

# 停止と削除を同時に（強制削除）
docker rm -f <コンテナID または 名前>
```

### コンテナのログを見る

```bash
docker logs <コンテナID または 名前>

# リアルタイムで追いかける
docker logs -f <コンテナID または 名前>
```

---

## ハンズオン: Ubuntu コンテナに入ってみよう

### ステップ 1: Ubuntu コンテナを起動

```bash
docker run -it --name myubuntu ubuntu bash
```

- `-i`: 標準入力を保持（キーボード入力を受け付ける）
- `-t`: 疑似ターミナルを割り当て（プロンプトが表示される）
- `ubuntu`: 使うイメージ
- `bash`: コンテナ内で実行するコマンド

**プロンプトが変わったら成功:**
```
root@a1b2c3d4e5f6:/#
```

### ステップ 2: コンテナ内で Linux コマンドを実行

```bash
# 現在いる場所を確認
pwd

# ファイル一覧を表示
ls /

# OS の情報を確認
cat /etc/os-release

# ファイルを作成してみる
echo "Hello Docker!" > /tmp/test.txt
cat /tmp/test.txt
```

### ステップ 3: コンテナから出る

```bash
exit
```

コンテナが停止します。

### ステップ 4: 停止したコンテナを確認

```bash
docker ps -a
```

STATUS が `Exited` になっているはず。

### ステップ 5: コンテナを削除

```bash
docker rm myubuntu
```

---

## よく使うコマンドまとめ

```bash
# 起動中のコンテナ一覧
docker ps

# 全コンテナ一覧（停止含む）
docker ps -a

# コンテナ起動（バックグラウンド）
docker run -d --name myapp nginx

# コンテナ停止
docker stop myapp

# コンテナ削除
docker rm myapp

# 停止中のコンテナをまとめて削除
docker container prune
```

---

## チェックリスト

- [ ] `docker run -it ubuntu bash` でコンテナに入れた
- [ ] コンテナ内で Linux コマンドを実行できた
- [ ] `exit` でコンテナを出られた
- [ ] `docker ps -a` で停止中のコンテナが確認できた
- [ ] `docker rm` でコンテナを削除できた

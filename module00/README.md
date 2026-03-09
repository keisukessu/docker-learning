# Module 0: セットアップ確認

## 目標
Docker Desktop が正しく動いていることを確認する。

## ステップ 1: Docker Desktop を起動する

1. タスクバーまたはスタートメニューから **Docker Desktop** を開く
2. クジラのアイコンが表示されて、ステータスが **"Running"** になるまで待つ

## ステップ 2: バージョン確認

ターミナル（PowerShell または コマンドプロンプト）を開いて実行：

```bash
docker --version
```

**期待される出力例:**
```
Docker version 27.x.x, build xxxxxxx
```

## ステップ 3: Docker の詳細情報確認

```bash
docker info
```

エラーが出なければ OK！

## ステップ 4: 最初のコンテナ起動

```bash
docker run hello-world
```

**期待される出力:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

この出力が見えれば、Docker のセットアップは完了です！

---

## トラブルシューティング

### エラー: "Cannot connect to the Docker daemon"

→ Docker Desktop が起動していない可能性があります。
→ Docker Desktop を起動してから再試行してください。

### エラー: "docker: command not found"

→ Docker Desktop が正しくインストールされていないか、PATH が通っていません。
→ Docker Desktop を再インストールしてください。

### Docker Desktop が起動しない

→ Windows の仮想化機能（Hyper-V / WSL2）が有効か確認してください。
→ BIOS で仮想化（Virtualization）が有効になっているか確認してください。

---

## チェックリスト

- [ ] Docker Desktop が起動している
- [ ] `docker --version` でバージョンが表示される
- [ ] `docker info` がエラーなく実行できる
- [ ] `docker run hello-world` が成功する

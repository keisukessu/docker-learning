# Module 7: 実践プロジェクト

## 目標
- 自分のアプリを完全に Docker 化する
- 環境変数を安全に管理する
- GitHub に公開できるポートフォリオを作る

---

## 実践プロジェクト: Todo アプリ

Flask + PostgreSQL で作った Todo アプリを Docker 化します。

### プロジェクト構成

```
module07/
├── docker-compose.yml
├── docker-compose.prod.yml    ← 本番用（オプション）
├── .env                       ← ローカル環境変数（Git に含めない）
├── .env.example               ← 環境変数のテンプレート（Git に含める）
├── .gitignore
├── README.md                  ← プロジェクトの説明
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    └── templates/
        └── index.html
```

---

## .env と .env.example

### .env（Git に含めない）
```env
POSTGRES_DB=tododb
POSTGRES_USER=todouser
POSTGRES_PASSWORD=secret_password_change_this
SECRET_KEY=your-secret-key-change-this
```

### .env.example（Git に含める・テンプレート）
```env
POSTGRES_DB=tododb
POSTGRES_USER=todouser
POSTGRES_PASSWORD=your_password_here
SECRET_KEY=your_secret_key_here
```

---

## .gitignore

```
.env
__pycache__/
*.pyc
.DS_Store
```

---

## app/requirements.txt

```
flask==3.0.0
psycopg2-binary==2.9.9
flask-sqlalchemy==3.1.1
```

---

## app/app.py

```python
import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベース接続設定
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.environ['POSTGRES_USER']}:"
    f"{os.environ['POSTGRES_PASSWORD']}@db/"
    f"{os.environ['POSTGRES_DB']}"
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/todo', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    if title:
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
    return index()


@app.route('/todo/<int:id>/done', methods=['POST'])
def toggle_done(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return index()


@app.route('/todo/<int:id>/delete', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return index()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## app/templates/index.html

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Docker Todo App</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        .done { text-decoration: line-through; color: gray; }
        li { margin: 8px 0; }
        input[type="text"] { padding: 8px; width: 300px; }
        button { padding: 8px 16px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Todo アプリ（Docker 版）</h1>

    <form method="post" action="/todo">
        <input type="text" name="title" placeholder="新しいタスクを入力" required>
        <button type="submit">追加</button>
    </form>

    <ul>
    {% for todo in todos %}
        <li>
            <span class="{{ 'done' if todo.done else '' }}">{{ todo.title }}</span>
            <form method="post" action="/todo/{{ todo.id }}/done" style="display:inline">
                <button type="submit">{{ '元に戻す' if todo.done else '完了' }}</button>
            </form>
            <form method="post" action="/todo/{{ todo.id }}/delete" style="display:inline">
                <button type="submit">削除</button>
            </form>
        </li>
    {% else %}
        <li>タスクがありません</li>
    {% endfor %}
    </ul>
</body>
</html>
```

---

## app/Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## docker-compose.yml

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
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./app:/app

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

---

## GitHub に公開するための README.md テンプレート

```markdown
# Todo App with Docker

Flask と PostgreSQL で作った Todo アプリを Docker で動かします。

## 必要なもの

- Docker Desktop

## 起動方法

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/todo-docker-app.git
cd todo-docker-app

# 環境変数を設定
cp .env.example .env
# .env を編集してパスワードなどを設定

# 起動
docker compose up -d --build

# ブラウザでアクセス
# http://localhost:5000
```

## 停止方法

```bash
docker compose down
```

## 技術スタック

- Python / Flask
- PostgreSQL
- Docker / Docker Compose
```

---

## GitHub へのアップロード手順

```bash
# Git リポジトリを初期化
git init

# .gitignore を確認（.env が含まれていることを確認）
cat .gitignore

# ファイルをステージング
git add .

# コミット
git commit -m "初回コミット: Docker で動く Todo アプリ"

# GitHub でリポジトリを作成してから
git remote add origin https://github.com/yourusername/todo-docker-app.git
git push -u origin main
```

---

## チェックリスト

- [ ] Todo アプリが Docker で動作する
- [ ] `.env` が Git に含まれていない
- [ ] `.env.example` が GitHub に公開されている
- [ ] `docker compose up -d --build` 一発で起動できる
- [ ] README.md に起動方法が書いてある
- [ ] GitHub にプッシュできた

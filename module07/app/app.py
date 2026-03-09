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


app.route('/todo/<int:id>/delete', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return index()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
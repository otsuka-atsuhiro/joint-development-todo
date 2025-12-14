from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- DB初期化 ---
def init_db():
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

init_db()

# --- 一覧表示 ---
@app.route("/")
def index():
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("SELECT id, title, done FROM todos")
    todos = c.fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

# --- 追加 ---
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()
    return redirect("/")

# --- 完了状態を切り替え ---
@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("SELECT done FROM todos WHERE id=?", (todo_id,))
    current = c.fetchone()[0]
    new = 0 if current == 1 else 1
    c.execute("UPDATE todos SET done=? WHERE id=?", (new, todo_id))
    conn.commit()
    conn.close()
    return redirect("/")

# --- 削除 ---
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # TODO: ここでデータベースからタスクを取得する
    tasks = [] # 仮のデータ
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
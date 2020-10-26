# flaskというフレームワークからFlaskをインポート
from flask import Flask, render_template, request, redirect
import sqlite3

# appというflaskアプリを作る的な宣言。
app = Flask(__name__)


@app.route('/')
def helloworld():
    return "Hello World."


@app.route('/<name>')
def greet(name):
    return name + "こんにちは"


@app.route('/template')
def template():
    py_name = "材木座くん"
    return render_template('index.html', name=py_name)


@app.route('/weather')
def weather():
    py_weather = "Sunny"
    return render_template('base.html', weather=py_weather)


@app.route('/dbtest')
def dbtest():
    # flasktest.dbに接続
    conn = sqlite3.connect('flasktest.db')
    # 中身が見られるようにしている
    c = conn.cursor()
    # SQL文の実行
    c.execute("select name, age, address from users")
    # 取ってきたレコードを格納
    user_info = c.fetchone()
    # データベース接続終了
    c.close()

    print(user_info)
    return render_template('dbtest.html', user_info=user_info)


@app.route('/add', methods=["GET"])
def add_get():
    return render_template('add.html')


@app.route('/add', methods=["POST"])
def add_post():
    # フォームのtaskに入力されたデータを取得
    task = request.form.get("task")

    # DBと接続
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("insert into task values(null, ?)", (task, ))
    # 変更を確定する
    conn.commit()
    conn.close()
    return redirect('/list')


@app.route('/list')
def task_list():
    user_name = "大将くん"
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("select id, task from task")
    task_list = []
    for row in c.fetchall():
        task_list.append({"id": row[0], "task": row[1]})
    c.close()
    return render_template(
        'tasklist.html',
        task_list=task_list,
        user_name=user_name)

@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("SELECT task FROM task WHERE id = ?",(id,))
    task = c.fetchone()
    c.close()
    if task is not None:
        task = task[0]
    else:
        return "指定したたすくがありません！"
    item={"id":id,"task":task}
    return render_template('edit.html',task = item)

@app.route('/edit',methods=['POST'])
def edit_post():
    item_id = request.form.get("html_task_id")
    # INPUTタグはテキスト型なので、INT方に直しています。
    item_id = int(item_id)
    task = request.form.get("html_task")

    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("UPDATE task SET task = ? WHERE id = ?",(task,item_id))
    conn.commit()
    c.close()
    return redirect('/list')

@app.route('/del/<int:id>')
def task_del(id):
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("DELETE FROM task WHERE id = ?",(id,))
    conn.commit()
    c.close()
    return redirect('/list')

@app.route('/regist')
def regist_get():
    return render_template('regist.html')

@app.route('/regist',methods=['POST'])
def regist_post():
    name = request.form.get("member_name")
    print(name)
    password = request.form.get("member_password")
    print(password)
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("INSERT INTO member VALUES(null,?,?)",(name,password))
    conn.commit()
    c.close()
    return "登録完了(๑>◡<๑)"

@app.errorhandler(404)
def notfound(code):
    return "404ページだよ。ごめんね"

    # flaskが持っている開発用のサーバーを起動する。
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        tasks=tasks
    )

@app.route('/add_task', methods=['POST'])
def add_task():

    task_name = request.form['task_name']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks(task_name,status) VALUES(?,?)",
        (task_name, "Pending")
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/delete_task/<int:id>')
def delete_task(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
import psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

def validate_user(username, password):
    conn = psycopg2.connect(
        host = "localhost",
        database = "logindatabase",
        user="postgres",
        password="root"
    )
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM logindata WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login/', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        return render_template('index.html')
    else:
        return render_template('index.html', error = 'Incorrect Password')

if __name__ == '__main__':
    app.run(debug=True)

import psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

def validate_user(username, password):
    conn = psycopg2.connect(
        host = "localhost",
        database = "logindata",
        user="postgres",
        password="root"
    )
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM logintable WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return True
    else:
        return False

def add_user(username, password):
    conn = psycopg2.connect(
        host = 'localhost',
        database = 'logindata',
        user = 'postgres',
        password = 'root'
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO logintable(username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/login/', methods=['POST', 'GET'])
def do_login():
    if request.method == 'POST':
        print('logging in')
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            print("Correct password")
            return render_template('dashboard.html')
                
        else:
            print("incorrect password")
            return render_template('login.html', error = 'Incorrect Password')

@app.route('/dosignup/', methods=['POST', 'GET'])
def do_signup():
    if request.method == 'POST':
        print('signing up')
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        print('added users')
        return render_template('login.html')           

@app.route('/logout/')
def log_out():
    print('logging out')
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)

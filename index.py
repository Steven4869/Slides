from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='slides'
)
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key=os.urandom(24)
@app.route('/')
def home():
    return render_template('login.html')
@app.route('/home')
def dashboard():
    cursor.execute("""SELECT * FROM `post`""")
    items = cursor.fetchall()
    if 'user_id' in session:
        return render_template('home.html', items=items)
    else:
        return redirect('/')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/add_user',methods=['POST'])
def add_user():
    name= request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""INSERT INTO `posts` (`name`,`username`,`password`) VALUES ('{}','{}','{}')""".format(name,username,password))
    conn.commit()
    return "User registered successfully"
@app.route('/login_validation', methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM `posts` WHERE `username` LIKE '{}' AND `password` LIKE '{}'""".format(username,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/')
@app.route('/slides')
def slides():
    return render_template('slides.html')
@app.route('/add_slide',methods=['POST'])
def add_slide():
    title = request.form.get('title')
    cursor.execute("""INSERT INTO `post` (`title`) VALUES ('{}')""".format(title))
    conn.commit()
    return "submitted succesfully"
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)

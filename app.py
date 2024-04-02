from flask import Flask,render_template,request
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flflflffl'

@app.route("/ok")
def main():
    title = "Musik"
    return render_template('main.html')

@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/register", methods= ['POST', 'GET'])
def register():
    if request.method == "POST":
        print(request.form['username'])
        db_session.global_init("db/blogs.db")
        user = User()
        user.name = request.form['username']
        user.email= request.form['email']
        user.hash_password = request.form['password']
        user.about = "1c23"
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
    else:
        print("ok")
    return render_template('register.html')
@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1',debug=True)

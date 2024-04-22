from flask import Flask,render_template,request,redirect,url_for,session
from data import db_session
from data.users import User
from data.musiks import Musiks
from validators import mp_val

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flflflffl'

@app.route("/")
def main():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    musik = db_sess.query(Musiks).all()
    print(session)
    if "name" in session:
        title = "Voshel"
        print("ok")
    else:
        title = "Musik"
        print("ne ok")
    return render_template('main.html',usernames = user,musik = musik)

@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == "POST":
        user = User()
        session.permanent = False
        db_sess = db_session.create_session()
        username = request.form['username']
        search = db_sess.query(User).filter_by(name = username).first()
        if search:
            session["name"] = username
            session["email"] = search.email
            return redirect(url_for("main"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template('login.html')
@app.route("/register", methods= ['POST', 'GET'])
def register():
    if request.method == "POST":
        print(request.form['username'])
        user = User()
        user.name = request.form['username']
        user.email = request.form['email']
        user.hash_password = request.form['password']
        user.about = "1c23"

        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for("login"))
    else:
        print("ok")
        return render_template('register.html')
@app.route("/admin")
def admin():
    return render_template("admin.html")
@app.route("/user", methods=["POST","GET"])
def user():
    print(session["name"])
    if "name" in session:
        name = session["name"]
        if request.method == "POST":
            file = request.files['file']
            if mp_val(file.filename) == "yes":
                upload = Musiks(name_musiks="koroll",file_musiks=file.filename)
                db_sess = db_session.create_session()
                db_sess.add(upload)
                db_sess.commit()
            else:
                print("no")
        return render_template("user.html", name=name)

    return redirect(url_for("register"))
@app.route("/exit")
def exit():
    session.pop("name",None)
    session.pop("email",None)
    return redirect(url_for('main'))
@app.errorhandler(404)
def not_found(error):
    return "ничего не нашлось"

if __name__ == "__main__":
    db_session.global_init("db/blogs.db")

    app.run(debug=True)

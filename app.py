from flask import Flask,render_template,request,redirect,url_for,session,flash
from data import db_session
from data.users import User
from data.musiks import Musiks
from validators import mp_val,photo_val
from data.my_musik import Musiks_Like

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ifbiwfbrb'
UPLOAD_FOLDER = '/musik/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/",methods=["POST","GET"])
def main():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    musik = db_sess.query(Musiks).all()
    musik_mass = musik
    if request.method == "POST":
        return render_template('main.html', usernames=user, musik=musik_mass)
    else:
        like="f"
        stage_user = "not sign"
        if "name" in session:
            title = "Voshel"
            user = db_sess.query(User).filter_by(name = session["name"]).first()
            stage_user = "sign"
        else:
            title = "Musik"

        return render_template('main.html',usernames = user,musik = musik_mass,like = like,stage_user = stage_user)

@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == "POST":
        user = User()
        session.permanent = False
        db_sess = db_session.create_session()
        username = request.form['username']
        password = request.form['password']
        search = db_sess.query(User).filter_by(name = username).first()
        if search:
            if search.name == username and password == search.hash_password:
                session["name"] = username
                session["email"] = search.email
                return redirect(url_for("main"))
            else:
                return redirect(url_for("login"))
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
    stage_user = "not_sign"
    if "name" in session:
        print(session["email"],session['name'])
        name = session["name"]
        db = db_session.create_session()
        user = db.query(User).filter_by(name = name).first()
        stage_user = "sign"
        email = session["email"]
        method = "get"
        if request.method == "POST":
            file = request.files['file']
            file_photo = request.files['photo']
            if mp_val(file.filename) == "yes" and photo_val(file_photo.filename)=="yes":
                upload = Musiks(name_musiks=request.form["name"],file_musiks=file.filename,photo_musiks = file_photo.filename)
                musik_like = Musiks_Like(name_musiks = upload.name_musiks,file_musiks = upload.file_musiks, user_id = user.id, photo_musiks = upload.photo_musiks)
                db_sess = db_session.create_session()
                db_sess.add(upload)
                db_sess.add(musik_like)
                db_sess.commit()
                filename = file.filename
                file.save(f'C:\\Users\\ntr07\PycharmProjects\musik_sait\static\musik\\{filename}')
                file_photo.save(f'C:\\Users\\ntr07\PycharmProjects\musik_sait\static\img\{file_photo.filename}')
                method = "post"
            else:
                flash("файл должен быть с расширением mp3")
        return render_template("user.html", name=name,stage_user = stage_user, email = email)
    else:
        return redirect(url_for("login"))
@app.route("/select_musiks",methods = ["POST","GET"])
def select_musiks():
    if "email" in session:
        if session["name"] == "admin":
            superuser = "yes"
            stage_user = "sign"
            db_sess = db_session.create_session()
            user_musik = db_sess.query(Musiks_Like).all()
            if request.method == 'POST':
                for el in request.values:
                    if el=="delete":
                        db_sess = db_session.create_session()
                        musikdb = db_sess.query(Musiks).filter(Musiks.name_musiks == request.form['namemusik']).first()
                        user_musik_del = db_sess.query(Musiks_Like).filter(Musiks_Like.name_musiks == request.form['namemusik']).first()
                        if musikdb:
                            db_sess.delete(musikdb)
                            db_sess.delete(user_musik_del)
                            db_sess.commit()
                            user_musik = db_sess.query(Musiks_Like).all()
        else:
            superuser = "not"
            stage_user = "sign"
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter_by(email=session["email"]).first()
            user_musik = db_sess.query(Musiks_Like).filter_by(user_id=user.id).all()

        return render_template("my_musiks.html",user_musik = user_musik,stage_user = stage_user,superuser = superuser)
    else:
        return redirect(url_for('login'))
@app.route("/exit")
def exit():
    session.pop("name",None)
    session.pop("email",None)
    return redirect(url_for('main'))
@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html")


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")

    app.run(debug=True)

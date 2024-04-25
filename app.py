from flask import Flask,render_template,request,redirect,url_for,session,flash
from data import db_session
from data.users import User
from data.musiks import Musiks
from validators import mp_val,random_musik,photo_val
from data.Like_musik import Musiks_Like

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flflflffl'
UPLOAD_FOLDER = '/musik/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/",methods=["POST","GET"])
def main():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    musik = db_sess.query(Musiks).all()
    for el in musik:
        print(el.file_musiks)
    musik_mass = musik
    if request.method == "POST":
        #like = db_sess.query(Musiks_Like).filter_by(name = )
        print(request.content_encoding)
        return render_template('main.html', usernames=user, musik=musik_mass)
    else:
        like="f"
        stage_user = "not sign"
        if "name" in session:
            title = "Voshel"
            print("ok")
            user = db_sess.query(User).filter_by(name = session["name"]).first()
            stage_user = "sign"
            if user:
                musik_liking = db_sess.query(Musiks_Like).filter_by(user_id=user.id).all()
                for fg in musik_liking:
                    if fg.like_musik == 1:
                        print(fg.name_musiks)
        else:
            title = "Musik"
            print("ne ok")

        return render_template('main.html',usernames = user,musik = musik_mass,like = like,stage_user = stage_user)

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
    stage_user = "not_sign"
    if "name" in session:
        name = session["name"]
        db = db_session.create_session()
        user = db.query(User).filter_by(name = name).first()
        stage_user = "sign"
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
                print("no")


        return render_template("user.html", name=name,stage_user = stage_user)
    else:
        return redirect(url_for("login"))
@app.route("/select_musiks")
def select_musiks():
    stage_user = "not sign"
    if "email" in session:
        stage_user = "sign"
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(email = session["email"]).first()
        user_musik = db_sess.query(Musiks_Like).filter_by(user_id = user.id).all()
        return render_template("my_musiks.html",user_musik = user_musik,stage_user = stage_user)
    else:
        return render_template("login.html")
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

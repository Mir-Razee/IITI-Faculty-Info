from sqlalchemy import create_engine

from sqlalchemy.testing import db
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
import sys

from webd import app
from flask import redirect, url_for, session, render_template, request, flash
from webd import oauth

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session.permanent = True
    return redirect('/form')

@app.route('/form')
def form():
    user=dict(session).get('profile',None);
    if user:
        return render_template('relocate.html')
    else:
        return "Please Login as admin"

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



engine = create_engine("mysql://root:Hosamani29m$@localhost/lab5", echo=True)

#Check connection
try:
    conn = engine.connect()
except Exception as e:
    print('Connection Failed\nError Details:', e)
    sys.exit(1)
conn.close()

db = scoped_session(sessionmaker(bind=engine))
log = False

@app.route("/admin", methods=["GET", "POST"])
def admin():
    print(log)
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        dept = request.form.get("dept")
        pwd = request.form.get("pwd")
        secure_password = sha256_crypt.encrypt(str(pwd))
        print(name, email, dept, pwd)

        table_data = db.execute("SELECT email FROM faculty WHERE email =:email",
        {"email":email}).fetchone()

        if table_data == None:
            db.execute("INSERT INTO faculty(email, facultyname, dept, password) VALUES(:email, :facultyname, :dept, :password)",
            {"email":email,"facultyname":name, "dept": dept, "password":secure_password})
            db.commit()
            flash("Faculty Registered Successfully", "success")
            return redirect(url_for("admin"))

        else:
            flash("Faculty already Registered", "danger")
            return redirect(url_for("admin"))

    return render_template("admin_form.html")

@app.route("/faculty", methods=["GET", "POST"])
def faculty():
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")

        table_data = db.execute("SELECT email FROM faculty WHERE email =:email",
                                {"email": email}).fetchone()
        password_data = db.execute("SELECT password FROM faculty WHERE email =:email",
                                   {"email": email}).fetchone()

        if table_data is None:
            flash("Faculty does not exist!", "error")
            return render_template("faculty_form.html")
        else:
            for pass_data in password_data:
                if sha256_crypt.verify(pwd, pass_data):
                    session = True
                    info = db.execute("SELECT * FROM faculty WHERE email =:email",
                                            {"email": email}).fetchone()
                    print(info[1], type(info))
                    return render_template("faculty_form.html", email=info[0], name=info[1], dept=info[2])
                else:
                    flash("Incorrect Password", "error")
                    return render_template("faculty_form.html")

    return render_template("faculty_form.html")






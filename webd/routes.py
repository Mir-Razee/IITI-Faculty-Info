from passlib.hash import sha256_crypt
from webd import app, db
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
    user = dict(session).get('profile', None);
    email = user.get("email")
    table_data = db.execute("SELECT email FROM faculty WHERE email =:email", {"email": email}).fetchone()
    if email == "cse200001054@iiti.ac.in":
        return render_template('admin_form.html',user=user)
    elif table_data:
        return render_template('faculty_form.html',user=user)
    else:
        return "Please go back and Login as admin or faculty"

@app.route('/Choices')
def QChoice():
    return render_template('qchoice.html')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        dept = request.form.get("dept")
        print(name, email, dept)

        table_data = db.execute("SELECT email FROM faculty WHERE email =:email",
        {"email":email}).fetchone()

        if table_data == None:
            db.execute("INSERT INTO faculty(email, facultyname, dept) VALUES(:email, :facultyname, :dept)",
            {"email":email,"facultyname":name, "dept": dept})
            db.commit()
            flash("Faculty Registered Successfully", "success")
            return redirect(url_for("admin"))

        else:
            flash("Faculty already Registered", "danger")
            return redirect(url_for("admin"))

    return render_template("admin_form.html")

@app.route("/faculty", methods=["GET", "POST"])
def faculty(session=session):
    if request.method == "POST":
        email = request.form.get("email")

        table_data = db.execute("SELECT email FROM faculty WHERE email =:email",
                                {"email": email}).fetchone()

    user = dict(session).get('profile', None)
    return render_template("faculty_form.html", user=user)

@app.route("/data1",methods=["GET","POST"])
def Data1():
    return render_template("data.html",s=False)

@app.route("/data2", methods=["GET", "POST"])
def Data2():
    dept = request.form['dept']
    q1 = db.execute("SELECT facultyname FROM faculty WHERE dept =:dept",
                    {"dept": dept}).fetchall()
    size =(len(q1))
    return render_template("data.html",s=True,dept=dept,q1=q1,size=size)

@app.route("/info", methods=["GET","POST"])
def qwery():
    Department = request.form['dept2']
    Faculty = request.form['fac']
    y1 = request.form['from_year']
    y2 = request.form['to_year']
    C_ID = db.execute("SELECT Course_ID FROM courses WHERE Dept =:Dept",
                            {"Dept": Department}).fetchall()
    Q = db.execute("SELECT facemail FROM relation WHERE course_ID =:course_ID",
                            {"course_ID": C_ID}).fetchall()
    print(C_ID[0][0],Q,Faculty,y1,y2,Department)
    return render_template("output.html", email = Q, fname=Faculty, y1=y1,y2=y2,cid=C_ID)


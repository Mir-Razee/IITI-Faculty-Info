from passlib.hash import sha256_crypt
from webd import app, db
from flask import redirect, url_for, session, render_template, request, flash
from webd import oauth
from flask_recaptcha import ReCaptcha # Import ReCaptcha object

app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY="6LdbqdEcAAAAAC3ZVzmeVq_DKPgl1B5SGrQ3uBpR",
    RECAPTCHA_SECRET_KEY="6LdbqdEcAAAAAIfvIDWi9uiC6Xrkm23rrHE0PXHA",

))

recaptcha = ReCaptcha(app=app)
recaptcha = ReCaptcha()
recaptcha.init_app(app)

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
    user = dict(session).get('profile', None)
    email = user.get("email")
    table_data = db.execute("SELECT email FROM faculty WHERE email =:email", {"email": email}).fetchone()
    dept = db.execute("SELECT dept from faculty where email= :email", {"email": email}).fetchone()
    dept = dept[0]
    if email == "cse200001054@iiti.ac.in":
        return render_template('admin_form.html',user=user)
    elif table_data:
        return render_template('faculty_form.html',user=user, dept=dept)
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

# @app.route("/faculty", methods=["GET", "POST"])
# def faculty(session=session):
#     if request.method == "POST":
#         email = request.form.get("email")
#
#         table_data = db.execute("SELECT email FROM faculty WHERE email =:email",
#                                 {"email": email}).fetchone()
#
#     user = dict(session).get('profile', None)
#     return render_template("faculty_form.html", user=user)

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

@app.route("/faculty", methods=["GET", "POST"])
def faculty(session=session):
    user = dict(session).get('profile', None)
    email = user.get("email")
    dept = db.execute("SELECT dept from faculty where email= :email", {"email": email}).fetchone()
    dept = dept[0]

    if request.method == "POST":
        cname = request.form.get("cname")
        cid = request.form.get("cid")
        stu = request.form.get("stu")
        room_no = request.form.get("room_no")
        year = request.form.get("year")
        sem = request.form.get("sem")
        no = request.form.get("no_of_classes")
        year = int(year)
        no = int(no)
        # stu = int(stu)

        z = db.execute("Select * from courses where Course_ID= :Course_ID", {"Course_ID": cid}).fetchone()
        y = db.execute("Select * from relation where facemail= :facemail and Course_ID= :Course_ID and year= :year and Semester= :Semester",
                       {"facemail": email, "Course_ID": cid, "year": year, "Semester": sem}).fetchone()
        print(y, z)
        if y is not None:
            flash("Course Already Registered by faculty for given year and semester", "error")
            return render_template("faculty_form.html", user=user, dept=dept)
        if z is None:
            db.execute("INSERT INTO courses(Course_ID, Course_name, Dept) VALUES(:Course_ID, :Course_name, :Dept)",
                   {"Course_ID": cid, "Course_name": cname, "Dept": dept})
            db.commit()

        print(cname, cid, room_no, year, sem, no)
        for i in range(no):
            d = "day_select_" + str(i+1)
            t = "time_select_" + str(i+1)
            day = request.form.get(d)
            time = request.form.get(t)
            slot_ids = db.execute("SELECT slot_id FROM timeslots WHERE day= :day AND time= :time",
                           {"day":day, "time":time}).fetchone()
            slot_id = slot_ids[0]
            print(type(slot_id), slot_id)
            check = db.execute("Select * from relation where facemail= :facemail and Course_ID= :Course_ID and year= :year and Semester= :Semester and Slot_Timing= :Slot_Timing",
                       {"facemail": email, "Course_ID": cid, "year": year, "Semester": sem, "Slot_Timing": slot_id}).fetchone()
            if check is None:
                db.execute("INSERT INTO relation(facemail, course_ID, no_of_students, room_no, year, Semester, Slot_Timing) VALUES(:facemail, :course_ID, :no_of_students, :room_no, :year, :Semester, :Slot_Timing)",
                       {"facemail": email, "course_ID": cid, "no_of_students": stu, "room_no": room_no, "year": year, "Semester": sem, "Slot_Timing": slot_id})
                db.commit()

        flash("Course Registered Successfully!", "success")
        return render_template("faculty_form.html", user=user, dept=dept)


    return render_template("faculty_form.html", user=user, dept=dept)


@app.route("/data6",methods=["GET","POST"])
def Data6():
    return render_template("data6.html")

@app.route('/getfac', methods=['GET','POST'])
def getfac():
    if request.method=='GET':
        dept= request.args.get('dept')
        faculty=db.execute("select facultyname from faculty where dept = :dept;", {"dept":dept}).fetchall()
        data=[]
        for row in faculty:
            data.append(list(row))
        print(data)
        return json.dumps(data)
    return "Nothing"

y2=2011; s2="autumn";
import json
@app.route('/gettime', methods=['GET','POST'])
def gettime():
    if request.method=='GET':
        day= request.args.get('day')
        sem= request.args.get('sem')
        year= int(request.args.get('year'))
        y2 = year; s2 = sem;
        print(day, sem, year, type(year))
        j = db.execute("SELECT Slot_Timing from relation where Semester= :Semester and year= :year", {"Semester": sem, "year": year}).fetchall()
        h = db.execute("SELECT Slot_ID from timeslots where day= :day", {"day": day}).fetchall()
        k = list(set(h) - set(j))
        l = []
        for i in range(len(k)):
            k[i] = k[i][0]
        k.sort()
        # print(j)
        # print(h)
        # print(k)
        data2 = []
        for i in k:
            l = db.execute("SELECT time from timeslots where slot_ID= :slot_ID", {"slot_ID": i}).fetchone()
            data2.append(list(l))
        # timeslots=db.execute("select time from timeslots where(day=:day and not exists ( select Slot_Timing from relation where slot_ID=Slot_Timing));", {"day":day}).fetchall()
        # data=[]
        # print(data2)
        # for row in timeslots:
        #     data.append(list(row))
        # print(data)
        return json.dumps(data2)
    return "Nothing"

@app.route("/edit", methods=["GET", "POST"])
def edit(session=session):
    user = dict(session).get('profile', None)
    email = user.get("email")
    dept = db.execute("SELECT dept from faculty where email= :email", {"email": email}).fetchone()
    dept = dept[0]
    cid_list = db.execute("select DISTINCT course_ID from relation where facemail= :facemail ;", {"facemail": email}).fetchall()
    for i in range(len(cid_list)):
        cid_list[i] = cid_list[i][0]
    print(cid_list)
    cname_list = []
    for j in cid_list:
        cn = db.execute("select Course_name from courses where Course_ID= :Course_ID ;", {"Course_ID": j}).fetchone()
        cname_list.append(cn[0])
    print(cname_list)
    t_list = []
    for i in range(len(cid_list)):
        u = "" + str(cid_list[i]) + ": " + cname_list[i]
        t_list.append(u)

    print(t_list)
    if request.method == "POST":
        cid = request.form.get("cname_id")
        cname = db.execute("select Course_name from courses where Course_ID= :Course_ID ;", {"Course_ID": j}).fetchone()
        cname = cname[0]
        stu = request.form.get("stu")
        room_no = request.form.get("room_no")
        year = request.form.get("year")
        sem = request.form.get("sem")
        no = request.form.get("no_of_classes")
        year = int(year)
        no = int(no)
        # stu = int(stu)

        z = db.execute("Select * from courses where Course_ID= :Course_ID", {"Course_ID": cid}).fetchone()
        if z is None:
            db.execute("INSERT INTO courses(Course_ID, Course_name, Dept) VALUES(:Course_ID, :Course_name, :Dept)",
                   {"Course_ID": cid, "Course_name": cname, "Dept": dept})
            db.commit()

        try:
            db.execute("Delete from relation where facemail=:facemail  and course_ID=:course_ID and year=:year and Semester=:Semester",
                       {"facemail": email, "course_ID": cid, "year": year, "Semester": sem})
            db.commit()
        except Exception as e:
            print(e)

        print(cname, cid, room_no, year, sem, no)
        for i in range(no):
            d = "day_select_" + str(i+1)
            t = "time_select_" + str(i+1)
            day = request.form.get(d)
            time = request.form.get(t)
            slot_ids = db.execute("SELECT slot_id FROM timeslots WHERE day= :day AND time= :time",
                           {"day":day, "time":time}).fetchone()
            slot_id = slot_ids[0]
            print(type(slot_id), slot_id)
            check = db.execute("Select * from relation where facemail= :facemail and Course_ID= :Course_ID and year= :year and Semester= :Semester and Slot_Timing= :Slot_Timing",
                       {"facemail": email, "Course_ID": cid, "year": year, "Semester": sem, "Slot_Timing": slot_id}).fetchone()
            if check is None:
                db.execute("INSERT INTO relation(facemail, course_ID, no_of_students, room_no, year, Semester, Slot_Timing) VALUES(:facemail, :course_ID, :no_of_students, :room_no, :year, :Semester, :Slot_Timing)",
                       {"facemail": email, "course_ID": cid, "no_of_students": stu, "room_no": room_no, "year": year, "Semester": sem, "Slot_Timing": slot_id})
                db.commit()

        flash("Course Edited Successfully!", "success")
        return render_template("edit.html", user=user, dept=dept, cid_list= cid_list, t_list=t_list)


    return render_template("edit.html", user=user, dept=dept, cid_list= cid_list, t_list=t_list)

@app.route('/captcha', methods=['GET', 'POST'])
def captcha():
    if request.method == 'POST': # Check to see if flask.request.method is POST
        if recaptcha.verify(): # Use verify() method to see if ReCaptcha is filled out
            return render_template("qchoice.html")
        else:
            flash("Captcha Failed! Please Retry")
            return render_template("home.html")
    return render_template('captcha.html')



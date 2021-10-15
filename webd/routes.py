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
    user = dict(session).get('profile', None)
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

# @app.route("/course", methods=["GET","POST"])
# def courses():
#     C_ID = request.form.get("cid")
#     C_name = request.form.get("name")
#     year = request.form.get("year")
#     room_no = request.form.get("room_no")

# import json
# @app.route('/gettime', methods=['GET','POST'])
# def gettime():
#     if request.method=='GET':
#         day= request.args.get('day')
#
#         timeslots=db.execute("select time from timeslots where(day=:day and not exists ( select Slot_Timing from relation where slot_ID=Slot_Timing));", {"day":day}).fetchall()
#         data=[]
#         for row in timeslots:
#             data.append(list(row))
#         print(data)
#         return json.dumps(data)
#     return "Nothing"


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

import json
@app.route('/gettime', methods=['GET','POST'])
def gettime():
    if request.method=='GET':
        day= request.args.get('day')
        sem= request.args.get('sem')
        year= int(request.args.get('year'))

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

@app.route("/faculty", methods=["GET", "POST"])
def faculty(session=session):
    user = dict(session).get('profile', None)
    if request.method == "POST":
        email = user.get("email")
        dept = db.execute("SELECT dept from faculty where email= :email", {"email": email}).fetchone()
        cname = request.form.get("cname")
        cid = request.form.get("cid")
        stu = request.form.get("stu")
        room_no = request.form.get("room_no")
        year = request.form.get("year")
        sem = request.form.get("sem")
        no = request.form.get("no_of_classes")
        year = int(year)
        no = int(no)
        stu = int(stu)
        z = db.execute("Select * from courses where Course_ID= :Course_ID", {"Course_ID": cid}).fetchone()
        y = db.execute("Select * from relation where facemail= :facemail and Course_ID= :Course_ID and year= :year and Semester= :Semester",
                       {"facemail": email, "Course_ID": cid, "year": year, "Semester": sem}).fetchone()
        print(y, z)
        if y is not None:
            return "Course Already Registered by faculty for given year and semester"
        if z is None:
            db.execute("INSERT INTO courses(Course_ID, Course_name, Dept) VALUES(:Course_ID, :Course_name, :Dept)",
                   {"Course_ID": cid, "Course_name": cname, "Dept": dept[0]})
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

        return "success"


    return render_template("faculty_form.html", user=user)


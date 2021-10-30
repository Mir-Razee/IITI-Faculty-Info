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

    if email == "cse200001054@iiti.ac.in":
        return render_template('admin_form.html',user=user)
    elif table_data:
        dept = db.execute("SELECT dept from faculty where email= :email", {"email": email}).fetchone()
        dept = dept[0]
        return render_template('faculty_form.html',user=user, dept=dept)
    else:
        return "Please go back and Login as admin or faculty"

@app.route('/Choices')
def QChoice():
    return render_template('qchoice.html')

@app.route("/data1",methods=["GET","POST"])
def Data1():
    return render_template("data1.html")

@app.route("/data2",methods=["GET","POST"])
def Data2():
    return render_template("data2.html")

@app.route("/data3",methods=["GET","POST"])
def Data3():
    return render_template("data3.html")

@app.route("/data4",methods=["GET","POST"])
def Data4():
    return render_template("data4.html")

@app.route("/data5",methods=["GET","POST"])
def Data5():
    return render_template("data5.html")

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

@app.route("/info", methods=["GET","POST"])
def qwery():

    Department = request.form['dept']
    Faculty = request.form['fac']
    y1 = request.form['from_year']
    y2 = request.form['to_year']
    if len(y1)==0 or len(y2)==0:
        y1 = 2011
        y2 = 2021
    if Department=="Select a Department" or Faculty=="Select a Faculty":
        return render_template("Err.html")

    FAC_MAIL = db.execute("SELECT email FROM faculty WHERE facultyname =:facultyname",
                          {"facultyname": Faculty}).fetchone()

    C_ID = db.execute("SELECT course_ID FROM relation WHERE facemail =:facemail AND year>=:y1 AND year<=:y2",
                            {"facemail":FAC_MAIL[0],"y1":y1,"y2":y2}).fetchall()


    if len(C_ID) == 0:
        return render_template("Err.html")


    def my_function(x):
        return list(dict.fromkeys(x))
    C_ID = list(my_function(C_ID))
    C_NAME = db.execute("SELECT Course_name FROM courses WHERE Course_ID = ANY (SELECT course_ID FROM relation WHERE facemail =:facemail AND year>=:y1 AND year<=:y2);",{"facemail":FAC_MAIL[0],"y1":y1,"y2":y2}).fetchall()


    return render_template("output1_2.html",cid=C_ID,size=len(C_ID),cname=C_NAME,X=Faculty, Y=Department, y1=y1, y2=y2)

@app.route("/info2", methods=["GET","POST"])
def qwery2():
    y1=2011
    y2=2021
    Department = request.form['dept']
    Faculty = request.form['fac']
    if Department=="Select a Department" or Faculty=="Select a Faculty":
        return render_template("Err.html")
    FAC_MAIL = db.execute("SELECT email FROM faculty WHERE facultyname =:facultyname",
                          {"facultyname": Faculty}).fetchone()
    C_ID = db.execute("SELECT course_ID FROM relation WHERE facemail =:facemail AND year>=:y1 AND year<=:y2",
                            {"facemail":FAC_MAIL[0],"y1":y1,"y2":y2}).fetchall()
    C_NAME = db.execute("SELECT Course_name FROM courses WHERE Course_ID = ANY (SELECT course_ID FROM relation WHERE facemail =:facemail AND year>=:y1 AND year<=:y2);",{"facemail":FAC_MAIL[0],"y1":y1,"y2":y2}).fetchall()

    if len(C_ID)==0 and len(C_NAME)==0 and len(Faculty)==0 and len(FAC_MAIL)==0:
        return render_template("Err.html")

    def my_function(x):
        return list(dict.fromkeys(x))
    C_ID = list(my_function(C_ID))
    print(C_ID,FAC_MAIL[0])
    return render_template("output1_2.html",cid=C_ID,size=len(C_ID),cname=C_NAME,X=Faculty, Y=Department, y1=y1, y2=y2)

@app.route("/info3", methods=["GET","POST"])
def qwery3():
    Department = request.form['dept']
    if Department=="Select a Department":
        return render_template("Err.html")
    y1 = request.form['from_year']
    y2 = request.form['to_year']
    C = db.execute("SELECT Course_ID,Course_name FROM courses WHERE( Dept =:Dept AND Course_ID = ANY (SELECT course_ID FROM relation WHERE year>=:y1 AND year<=:y2));",
                            {"Dept":Department,"y1":y1,"y2":y2}).fetchall()

    if len(C)==0 and len(y1)==0 and len(y2)==0:
        return render_template("Err.html")

    def my_function(x):
        return list(dict.fromkeys(x))
    C = list(my_function(C))

    return render_template("output3.html",cid=C,size=len(C),Dept=Department,y1=y1,y2=y2)

@app.route("/info4", methods=["GET","POST"])
def qwery4():
    Department = request.form['dept']
    C_ID = request.form['cou']
    if Department=="Select a Department" or C_ID=="Select a Course":
        return render_template("Err.html")
    FAC_NAME = db.execute("SELECT facultyname,email FROM faculty WHERE email = ANY (SELECT facemail FROM relation WHERE course_ID =:course_ID );",{"course_ID":C_ID}).fetchall()

    print(C_ID,FAC_NAME)
    return render_template("output4.html",fac=FAC_NAME,size=len(FAC_NAME), Y=Department, Z=C_ID)

@app.route("/info5", methods=["GET","POST"])
def qwery5():
    Year = request.form['year']
    Sem = request.form['sem']

    CID = db.execute("SELECT DISTINCT course_ID FROM relation WHERE year=:year AND Semester=:sem",{"year":Year,"sem":Sem}).fetchall()
    for i in range(len(CID)):
        CID[i] = CID[i][0]
    col_dept=[]
    col_cname=[]
    col_cid = []
    col_fmail = []
    col_dept  = []
    col_fname = []
    for i in CID:
        FMAIL = db.execute("SELECT DISTINCT facemail FROM relation WHERE course_ID= :course_ID",{"course_ID": i}).fetchall()
        for x in FMAIL:
            col_cid.append(i)
            col_fmail.append(x[0])
    for i in col_cid:
        CNAME = db.execute("SELECT dept, Course_name FROM courses WHERE Course_ID= :Course_ID",{"Course_ID": i}).fetchone()
        col_cname.append(CNAME[1])
        col_dept.append(CNAME[0])
    for i in col_fmail:
        FNAME = db.execute("SELECT facultyname FROM faculty WHERE email= :email",
                           {"email": i}).fetchone()
        col_fname.append(FNAME[0])

    col_room=[]
    col_stu=[]
    col_time=[]
    for i in range(len(col_cid)):
        dbc = db.execute("SELECT no_of_students, room_no from relation where course_ID=:course_ID and year=:year and Semester=:Semester and facemail=:facemail",
                         {"course_ID": col_cid[i], "year": Year, "Semester": Sem, "facemail": col_fmail[i]}).fetchone()
        col_stu.append(dbc[0])
        col_room.append(dbc[1])

    for i in range(len(col_cid)):
        dbc = db.execute("SELECT Slot_Timing from relation where course_ID=:course_ID and year=:year and Semester=:Semester and facemail=:facemail",
                         {"course_ID": col_cid[i], "year": Year, "Semester": Sem, "facemail": col_fmail[i]}).fetchall()
        for j in range(len(dbc)):
            dbc[j] = dbc[j][0]

        col_time.append(dbc)
        # for x in dbc:
        #     rt = db.execute("SELECT day, time from timeslots where ")
        print(dbc, len(dbc))

    print(col_time)


    return render_template("output5.html", col_cid=col_cid, col_cname=col_cname, col_fmail=col_fmail, col_fname=col_fname,
                           col_dept=col_dept, col_room=col_room, col_stu = col_stu, col_time = col_time,Y=Year,S=Sem)


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

@app.route('/getcou', methods=['GET','POST'])
def getcou():
    if request.method=='GET':
        dept= request.args.get('dept')
        faculty=db.execute("select Course_ID from courses where dept = :dept;", {"dept":dept}).fetchall()
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




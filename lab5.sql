use lab5;
drop table relation;
drop table timeslots;
drop table faculty;
drop table courses;

CREATE TABLE if not exists faculty(
email varchar(45) NOT NULL,
facultyname varchar(45),
dept varchar(45),
primary key(email)
);

CREATE TABLE if not exists courses(
Course_ID int NOT NULL,
Course_name varchar(45),
Dept varchar(45),
primary key(Course_ID)
);
CREATE TABLE if not exists timeslots(
day varchar(45),
time varchar(45),
slot_ID varchar(45) not null,
primary key(slot_ID)
);

CREATE TABLE if not exists relation(
facemail varchar(45),
FOREIGN KEY(facemail) references faculty(email),
course_ID INT,
FOREIGN KEY(course_ID) references courses(Course_ID),
no_of_students int,
room_no varchar(45),
year int NOT NULL,
Semester varchar(45) NOT NULL,
primary key(facemail, course_ID, year, Semester, Slot_Timing),
Slot_Timing varchar(45),
FOREIGN KEY(Slot_Timing) references timeslots(slot_ID)
);

INSERT INTO faculty
VALUES ("vipul@iiti.ac.in", "Vipul Singh","EE");
INSERT INTO faculty
VALUES ("gverma@iiti.ac.in", "Girish Verma","ME");
INSERT INTO faculty
VALUES ("dipak@iiti.ac.in", "Dipak Roy","Chemistry");
INSERT INTO faculty
VALUES ("ganti@iiti.ac.in", "Ganti Murthy","BSBE");
INSERT INTO faculty
VALUES ("ankhiroy@iiti.ac.in", "Ankhi Roy","Physics");
INSERT INTO faculty
VALUES ("vkohli@iiti.ac.in", "Virat Kohli","Astronomy");
INSERT INTO faculty
VALUES ("vkg@iiti.ac.in", "Vinay Gupta","Mathematics");
INSERT INTO faculty
VALUES ("satyanarayan@iiti.ac.in", "S Patel","CE");
INSERT INTO faculty
VALUES ("punit@iiti.ac.in", "Punit Gupta","CSE");
INSERT INTO faculty
VALUES ("narendra@iiti.ac.in", "Narendra Chaudhari","CSE");
INSERT INTO faculty
VALUES ("aghoshal@iiti.ac.in", "Ananya Ghoshal","HSC");
INSERT INTO faculty
VALUES ("nagendra@iiti.ac.in", "Nagendra Kumar","CSE");
SELECT * FROM FACULTY;

select * from timeslots;
INSERT INTO timeslots VALUES("Wednesday","8-9 am","Wed0");
INSERT INTO timeslots VALUES("Wednesday","9-10 am","Wed1");
INSERT INTO timeslots VALUES("Wednesday","10-11 am","Wed2");
INSERT INTO timeslots VALUES("Wednesday","11-12 pm","Wed3");
INSERT INTO timeslots VALUES("Wednesday","12-1 pm","Wed4");
INSERT INTO timeslots VALUES("Wednesday","1-2 pm","Wed5");
INSERT INTO timeslots VALUES("Wednesday","2-3 pm","Wed6");
INSERT INTO timeslots VALUES("Wednesday","3-4 pm","Wed7");
INSERT INTO timeslots VALUES("Wednesday","4-5 pm","Wed8");
INSERT INTO timeslots VALUES("Wednesday","5-6 pm","Wed9");

INSERT INTO timeslots VALUES("Thursday","8-9 am","Thu0");
INSERT INTO timeslots VALUES("Thursday","9-10 am","Thu1");
INSERT INTO timeslots VALUES("Thursday","10-11 am","Thu2");
INSERT INTO timeslots VALUES("Thursday","11-12 pm","Thu3");
INSERT INTO timeslots VALUES("Thursday","12-1 pm","Thu4");
INSERT INTO timeslots VALUES("Thursday","1-2 pm","Thu5");
INSERT INTO timeslots VALUES("Thursday","2-3 pm","Thu6");
INSERT INTO timeslots VALUES("Thursday","3-4 pm","Thu7");
INSERT INTO timeslots VALUES("Thursday","4-5 pm","Thu8");
INSERT INTO timeslots VALUES("Thursday","5-6 pm","Thu9");

INSERT INTO timeslots VALUES("Friday","8-9 am","Fri0");
INSERT INTO timeslots VALUES("Friday","9-10 am","Fri1");
INSERT INTO timeslots VALUES("Friday","10-11 am","Fri2");
INSERT INTO timeslots VALUES("Friday","11-12 pm","Fri3");
INSERT INTO timeslots VALUES("Friday","12-1 pm","Fri4");
INSERT INTO timeslots VALUES("Friday","1-2 pm","Fri5");
INSERT INTO timeslots VALUES("Friday","2-3 pm","Fri6");
INSERT INTO timeslots VALUES("Friday","3-4 pm","Fri7");
INSERT INTO timeslots VALUES("Friday","4-5 pm","Fri8");
INSERT INTO timeslots VALUES("Friday","5-6 pm","Fri9");

INSERT INTO timeslots VALUES("Saturday","8-9 am","Sat0");
INSERT INTO timeslots VALUES("Saturday","9-10 am","Sat1");
INSERT INTO timeslots VALUES("Saturday","10-11 am","Sat2");
INSERT INTO timeslots VALUES("Saturday","11-12 pm","Sat3");
INSERT INTO timeslots VALUES("Saturday","12-1 pm","Sat4");
INSERT INTO timeslots VALUES("Saturday","1-2 pm","Sat5");
INSERT INTO timeslots VALUES("Saturday","2-3 pm","Sat6");
INSERT INTO timeslots VALUES("Saturday","3-4 pm","Sat7");
INSERT INTO timeslots VALUES("Saturday","4-5 pm","Sat8");
INSERT INTO timeslots VALUES("Saturday","5-6 pm","Sat9");

INSERT INTO timeslots VALUES("Tuesday","8-9 am","Tue0");
INSERT INTO timeslots VALUES("Tuesday","9-10 am","Tue1");
INSERT INTO timeslots VALUES("Tuesday","10-11 am","Tue2");
INSERT INTO timeslots VALUES("Tuesday","11-12 pm","Tue3");
INSERT INTO timeslots VALUES("Tuesday","12-1 pm","Tue4");
INSERT INTO timeslots VALUES("Tuesday","1-2 pm","Tue5");
INSERT INTO timeslots VALUES("Tuesday","2-3 pm","Tue6");
INSERT INTO timeslots VALUES("Tuesday","3-4 pm","Tue7");
INSERT INTO timeslots VALUES("Tuesday","4-5 pm","Tue8");
INSERT INTO timeslots VALUES("Tuesday","5-6 pm","Tue9");

INSERT INTO timeslots VALUES("Monday","8-9 am","Mon0");
INSERT INTO timeslots VALUES("Monday","9-10 am","Mon1");
INSERT INTO timeslots VALUES("Monday","10-11 am","Mon2");
INSERT INTO timeslots VALUES("Monday","11-12 pm","Mon3");
INSERT INTO timeslots VALUES("Monday","12-1 pm","Mon4");
INSERT INTO timeslots VALUES("Monday","1-2 pm","Mon5");
INSERT INTO timeslots VALUES("Monday","2-3 pm","Mon6");
INSERT INTO timeslots VALUES("Monday","3-4 pm","Mon7");
INSERT INTO timeslots VALUES("Monday","4-5 pm","Mon8");
INSERT INTO timeslots VALUES("Monday","5-6 pm","Mon9");

INSERT INTO COURSES VALUES("203", "DBMS", "CSE");
insert into relation
values("nagendra@iiti.ac.in","203","80", "L01", "2021","autumn","Mon4");
insert into relation
values("nagendra@iiti.ac.in","203","80", "L01", "2021","autumn","Wed1");



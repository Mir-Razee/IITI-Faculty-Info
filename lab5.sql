use lab5;

CREATE TABLE faculty(
email varchar(45) NOT NULL,
facultyname varchar(45),
dept varchar(45),
password varchar(255),
primary key(email)
);
CREATE TABLE courses(
Course_ID int NOT NULL,
Course_name varchar(45),
Dept varchar(45),
primary key(Course_ID)
);
CREATE TABLE timeslots(
day varchar(45),
time varchar(45),
slot_ID varchar(45) not null,
primary key(slot_ID)
);
CREATE TABLE relation(
facemail varchar(45),
FOREIGN KEY(facemail) references faculty(email),
course_ID int,
FOREIGN KEY(course_ID) references courses(Course_ID),
no_of_students int,
years int NOT NULL,
Semester varchar(45),
primary key(year),
Slot_Timing varchar(45),
FOREIGN KEY(Slot_Timing) references timeslots(slot_ID)
);
INSERT INTO faculty
VALUES ("vipul@iiti.ac.in", "Vipul Singh","EE", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("gverma@iiti.ac.in", "Girish Verma","ME", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("dipak@iiti.ac.in", "Dipak Roy","Chemistry", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("ganti@iiti.ac.in", "Ganti Murthy","BSBE", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("ankhiroy@iiti.ac.in", "Ankhi Roy","Physics", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("vkohli@iiti.ac.in", "Virat Kohli","Astronomy", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("vkg@iiti.ac.in", "Vinay Gupta","Mathematics", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("satyanarayan@iiti.ac.in", "S Patel","CE", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("punit@iiti.ac.in", "Punit Gupta","CSE", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("narendra@iiti.ac.in", "Narendra Chaudhari","CSE", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("aghoshal@iiti.ac.in", "Ananya Ghoshal","HSC", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
INSERT INTO faculty
VALUES ("nagendra@iiti.ac.in", 'Nagendra Kumar',"CSE", "$5$rounds=535000$4yKvLnb1T0TOBz8e$GMVuaTJaxKpLHM52ILpm5693skkink/JTR/lOkee4fD");
SELECT * FROM faculty;
insert into courses
values("201","Computers","CSE");
SELECT facultyname FROM faculty WHERE dept = 'CSE';

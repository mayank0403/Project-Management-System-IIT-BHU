# Project Management System IIT BHU
This project is a online project management system for undergraduate and graduate students and their supervisors. It is Django Framework in Python and RDBMS is built in MySQL.

The project serves the purpose of making the tedious tasks of grade assignment, attendance, advisor assignment, student preferences for advisor and project online to speed up the initial and continuous process of interaction that happens between a typical student-advisor relationship.

NOTE - If you need the dbdump file to run this project on your system, then send me an email.

--------

Open readme.pdf and Requirements.pdf for more information.

### Project Setup
1. Start Server Through python:

run `python manage.py runserver` in `project_management/`

2. Open Browser and navigate to `http://127.0.0.1:8000/adminlogin/` to open admin login page and `http://127.0.0.1:8000/login/` to open voter login page.

3. Browse through the project!

### Notes:
This system consists of two types of account.
1. Admin account who has the right to create an new student and professor accounts, delete these accounts and assign panels to for final assessment of the grades regarding each project.
2. Student account who can register on the portal and fill preferences to the advisors they would like to work with, submit their attendance, flag their progress and upload their resumes.
3. Professor account who can see the list of students along with their preference number, GPA and resumes, and select the students who he/she would like to mentor, keep a track of the progress and attendance of students and assign final grades via individual as well as panel assessment.

The details of the project are as follows:

* **Django** version : *1.10.2*

* **MySQL Server** Version: *5.7.13-0ubuntu0.16.04.2*

* **MySQL-python** version : *1.2.5*

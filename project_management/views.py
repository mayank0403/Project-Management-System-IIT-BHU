from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime

def my_custom_sql(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM test")
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    row2 = [y for y in [x for x in row]]
    return render(request, 'project_management/test.html',{'data':row1, 'data1':row2})

def home(request):
    return render(request, 'project_management/home.html')

def studentlogin(request):
    return render(request, 'project_management/studentlogin.html')

def employeelogin(request):
    return render(request, 'project_management/employeelogin.html')

def studentsignup(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    return render(request, 'project_management/addstudent.html')

def studentsignupranged(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    return render(request, 'project_management/addstudentranged.html')

def employeesignup(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    return render(request, 'project_management/addemployee.html')

def userlogout(request):
    logout(request)
    return render(request, 'project_management/home.html', {'data':"Logged out"})

def createstudentusers(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    username = request.POST['username']
    password = request.POST['password']
    with connection.cursor() as cursor:
        cursor.execute("select count(*) from auth_user where username = %s", [username])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    if(row1[0]==0):
        User.objects.create_user(username, '', password)
    else:
        return render(request, 'project_management/addstudent.html', {'data':"Username already taken."})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from student where rollno=%s;', [username])
        r = cursor.fetchall()
    print r[0]
    print "abcd"
    if(r[0][0]!=0):
        return render(request, 'project_management/addstudent.html', {'data':"Username already taken."})
    with connection.cursor() as cursor:
	    cursor.execute('insert into student values(%s, "Anonymous New User", "0.0", NULL, 0, aes_encrypt(%s, "cryptography"), "Computer Science and Engineering", NULL, 0, 40, NULL)', [username, password])
    return render(request, 'project_management/admin.html', {'data':"New User Created"})

def createemployeeusers(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    username = request.POST['username']
    password = request.POST['password']
    with connection.cursor() as cursor:
        cursor.execute("select count(*) from auth_user where username = %s", [username])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    if(row1[0]==0):
        User.objects.create_user(username, '', password)
    else:
        render(request, 'project_management/addemployee.html', {'data':"Username already taken."})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from guide where id=%s;', [username])
        r = cursor.fetchall()
    if(r[0][0]!=0):
        return render(request, 'project_management/addemployee.html', {'data':"Username already taken."})
    with connection.cursor() as cursor:
	    cursor.execute('insert into guide values(%s, "Anonymous New User", 4,aes_encrypt(%s, "cryptography"), "Computer Science and Engineering")', [username, password])
    return render(request, 'project_management/admin.html', {'data':"User Created"})

def createstudentusersranged(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    begin = request.POST['start']
    end = request.POST['end']
    for i in range(int(begin), int(end)+1):
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from auth_user where username = %s", [i])
            row = cursor.fetchall()
        row1 = [y for x in row for y in x]
        if(row1[0]==0):
            User.objects.create_user(i, '', str(i)+"123xyz")
        else:
            return render(request, 'project_management/addstudentranged.html', {'data':"Username already taken."})
        with connection.cursor() as cursor:
            cursor.execute('select count(*) from student where rollno=%s;', [i])
            r = cursor.fetchall()
        if(r[0][0]!=0):
            return render(request, 'project_management/addstudent.html', {'data':"Username already taken."})
        with connection.cursor() as cursor:
	        cursor.execute('insert into student values(%s, "Anonymous New User", 0.0, NULL, 0, aes_encrypt(%s, "cryptography"), "Computer Science and Engineering", NULL, 0, 40, NULL)', [i, str(i)+"123xyz"])
    return render(request, 'project_management/admin.html', {'data':"Users Created"})
    
def adminlogin(request):
    return render(request, 'project_management/adminlogin.html')

def adminverify(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM admin WHERE username = %s and password = %s;', [request.POST['username'], request.POST['password']])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    if(len(row1)>=1):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return render(request, 'project_management/admin.html')
    else:
	    return render(request, 'project_management/home.html', {'data':"Enter correct credentials"})
#def createemployeeusers(request):

def verifystudentloginedit(request):
    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM student WHERE rollno = %s and aes_decrypt(password, %s) = %s;', [request.user.username, "cryptography", request.POST['password']])        
            row = cursor.fetchall()
        row1 = [y for x in row for y in x]
        if(float(request.POST['cgpa'])<0.0 or float(request.POST['cgpa'])>10.00):
            return render(request, 'project_management/studentdetail.html', {'data':"Enter a valid CGPA"})
        with connection.cursor() as cursor:
            cursor.execute('select count(*) from department where name=%s;', [request.POST['dept']])
            r = cursor.fetchall()
        print "fsafa"
        print r[0][0]
        if(r[0][0]==0):
            return render(request, 'project_management/studentdetail.html', {'data':"Enter a valid Department"})
        with connection.cursor() as cursor:
	    # change password in auth_user as well
            cursor.execute('update student set name = %s, password = aes_encrypt(%s, %s), cgpa = %s, proj_topic_ideas = %s, dept_name = %s where rollno = %s;',[request.POST['name'], request.POST['password'], "cryptography",  request.POST['cgpa'], request.POST['ideas'], request.POST['dept'], request.user.username])
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM student WHERE rollno = %s and aes_decrypt(password, %s) = %s;', [request.user.username, "cryptography", request.POST['password']])        
            row = cursor.fetchall()
        row1 = [y for x in row for y in x]
        maps = {'Roll Number':row1[0], 'Name':row1[1], 'CGPA':row1[2], 'Project Ideas':row1[3], 'Allocation Flag':row1[4], 'Department Name':row1[6], 'Project ID(if allocated)':row1[7], 'Attendance':row1[8], 'Maximum Attendance':row1[9], 'Next Meet Date':row1[10]}
        u = User.objects.get(username=request.user.username)
        u.set_password(request.POST['password'])
        u.save()
        return render(request, 'project_management/studentdetail.html', {'data':"Updated Profile", 'map':maps})
    else:
        return render(request, 'project_management/studentlogin.html', {'data':"Error updating, log in again"})

def verifystudentlogin(request):
    with connection.cursor() as cursor:
        
        cursor.execute('SELECT * FROM student WHERE rollno = %s and aes_decrypt(password, %s) = %s;', [request.POST['username'], "cryptography", request.POST['password']])        
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    if(len(row1)>=1):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        maps = {'Roll Number':row1[0], 'Name':row1[1], 'CGPA':row1[2], 'Project Ideas':row1[3], 'Allocation Flag':row1[4], 'Department Name':row1[6], 'Project ID(if allocated)':row1[7], 'Attendance':row1[8], 'Maximum Attendance':row1[9], 'Next Meet Date':row1[10]}
        return render(request, 'project_management/studentdetail.html',{'data1':row1,'map':maps})
    else:
        return render(request, 'project_management/studentlogin.html', {'data':"Enter correct details"})

def verifyemployeelogin(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM guide WHERE id = %s and aes_decrypt(password, %s) = %s;', [request.POST['username'], "cryptography", request.POST['password']])        
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    if(len(row1)>=1):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        maps = {'Guide ID':row1[0], 'Name':row1[1], 'Seats Left':row1[2], 'Department':row1[4]}
        return render(request, 'project_management/employeedetail.html',{'data1':row1,'map':maps})
    else:
        return render(request, 'project_management/employeelogin.html', {'data':"Enter correct details"})

def verifyemployeeloginedit(request):
    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('select count(*) from department where name=%s;', [request.POST['dept']])
            r = cursor.fetchall()
        if(r[0][0]==0):
            return render(request, 'project_management/employeedetail.html', {'data':"Enter a valid Department"})
        with connection.cursor() as cursor:
	    # change password in auth_user as well
            cursor.execute('update guide set name = %s, password = aes_encrypt(%s, %s), seats_left = 4, dept_name = %s where id = %s;',[request.POST['name'], request.POST['password'], "cryptography", request.POST['dept'], request.user.username])
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM guide WHERE id = %s and aes_decrypt(password, %s) = %s;', [request.user.username, "cryptography", request.POST['password']])        
            row = cursor.fetchall()
        row1 = [y for x in row for y in x]
        maps = {'Guide ID':row1[0], 'Name':row1[1], 'Seats Left':row1[2], 'Department':row1[4]}
        u = User.objects.get(username=request.user.username)
        u.set_password(request.POST['password'])
        u.save()
        return render(request, 'project_management/employeedetail.html', {'data':"Updated Profile", 'map':maps})
    else:
        return render(request, 'project_management/employeelogin.html', {'data':"Error updating, log in again"})

def fillpreference(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select id, name from guide')
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row3 = [{'Professor Name':row2[i][1], 'Professor ID':row2[i][0]} for i in range(len(row2))]
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from preferences where student_roll=%s', [request.user.username])
        row = cursor.fetchall()
    row12 = [y for x in row for y in x]
    if(row12[0]!=0):
        with connection.cursor() as cursor:
            cursor.execute('select name from preferences, guide where student_roll=%s and guide.id = guide_id', [request.user.username])
            row13 = cursor.fetchall()
        row11 = [y for x in row13 for y in x]
        maps={'Preference1':row11[0], 'Preference2':row11[1], 'Preference3':row11[2], 'Preference4':row11[3]}
        return render(request, 'project_management/showpreference.html', {'map':maps})
    return render(request, 'project_management/fillpreference.html', {'data2':row3})

def addpreference(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from guide where id=%s or id=%s or id=%s or id=%s;', [request.POST['username1'], request.POST['username2'], request.POST['username3'], request.POST['username4']])
        r=cursor.fetchall()
    if(r[0][0]!=4):
        with connection.cursor() as cursor:
            cursor.execute('select id, name from guide')
            row = cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row3 = [{'Professor Name':row2[i][1], 'Professor ID':row2[i][0]} for i in range(len(row2))]
        return render(request, 'project_management/fillpreference.html', {'data':"Enter valid preferences", 'data2':row3})
    with connection.cursor() as cursor:
        cursor.execute('insert into preferences values(1, %s, %s)', [request.POST['username1'], request.user.username])
        cursor.execute('insert into preferences values(2, %s, %s)', [request.POST['username2'], request.user.username])
        cursor.execute('insert into preferences values(3, %s, %s)', [request.POST['username3'], request.user.username])
        cursor.execute('insert into preferences values(4, %s, %s)', [request.POST['username4'], request.user.username])
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM student WHERE rollno = %s;', [request.user.username])        
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    maps = {'Roll Number':row1[0], 'Name':row1[1], 'CGPA':row1[2], 'Project Ideas':row1[3], 'Allocation Flag':row1[4], 'Department Name':row1[6], 'Project ID(if allocated)':row1[7], 'Attendance':row1[8], 'Maximum Attendance':row1[9], 'Next Meet Date':row1[10]}
    return render(request, 'project_management/studentdetail.html', {'data':"Added the preferences", 'map':maps}) 

def showprofessordetails(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select name, seats_left, publication, interest_area from guide, guide_pub, guide_interest where id = guide_pub.guide_id and id = guide_interest.guide_id;')
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row3 = [{'Professor Name':row2[i][0], 'Seats Left':row2[i][1], 'Publication':row2[i][2], 'Interest Area':row2[i][3]} for i in range(len(row2))]
    return render(request, 'project_management/showprofessordetails.html', {'data1':row3})

def prefinfo(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select pref_number, student.name, allocated_flag from guide, preferences, student where id = preferences.guide_id and rollno = preferences.student_roll and id=%s', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row3 = [{'Student Name':row2[i][1], 'Preference Number':row2[i][0], 'Allocation Flag':row2[i][2]} for i in range(len(row2))]
    return render(request, 'project_management/prefinfo.html', {'data1':row3})

def showstudentinfo(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select rollno, student.name, cgpa, proj_topic_ideas, allocated_flag, student.dept_name, interest_area, project_topic from guide, preferences, student, stud_interest, past_projects where rollno=stud_interest.student_roll and rollno=past_projects.student_roll and id = preferences.guide_id and rollno = preferences.student_roll and id=%s;', [request.user.username])
        row11 = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute('select rollno from student, guide, preferences where id = preferences.guide_id and rollno = preferences.student_roll and id=%s and allocated_flag=0;', [request.user.username])
        row21 = cursor.fetchall()
    row2 = [y for y in[x for x in row11]]
    row3 = [y for y in[x for x in row21]]
    row41 = [{'Student Name':row2[i][1], 'Roll Number':row2[i][0], 'CGPA':row2[i][2], 'Ideas':row2[i][3], 'Allocation Flag':row2[i][4], 'Department':row2[i][5], 'Interest':row2[i][6], 'Past Project Topic':row2[i][7]} for i in range(len(row2))]
    row31 = [{'Roll Number':row3[i][0]} for i in range(len(row3))]
    return render(request, 'project_management/showstudentinfo.html', {'data1':row31, 'data2':row41})


def changeallocation(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select rollno from student, guide, preferences where id = preferences.guide_id and rollno = preferences.student_roll and id=%s and allocated_flag=0;', [request.user.username])
        row2 = cursor.fetchall()
    row3 = [y for x in row2 for y in x]
    with connection.cursor() as cursor:
        cursor.execute('select seats_left from guide where id = %s;',[request.user.username])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    count=0
    for i in row3:
        a = request.POST.get('choice'+i)
        print a
        print i
        if(a != "Lock" and a != "Wait" and a != "Free"):
            print "out"
            return render(request, 'project_management/employeelogin.html', {'data':"Unchanged Allocation"})
        if(a == "Lock"):
            count = count + 1
        if(a=='Wait'):
            with connection.cursor() as cursor:
                cursor.execute('update student set allocated_flag=1 where rollno=%s;',[i])
        if(a=='Free'):
            with connection.cursor() as cursor:
                cursor.execute('update student set allocated_flag=0 where rollno=%s;',[i])
    print count

    if(count>int(row1[0])):
        with connection.cursor() as cursor:
            cursor.execute('select rollno, student.name, cgpa, proj_topic_ideas, allocated_flag, student.dept_name, interest_area, project_topic from guide, preferences, student, stud_interest, past_projects where rollno=stud_interest.student_roll and rollno=past_projects.student_roll and id = preferences.guide_id and rollno = preferences.student_roll and id=%s;', [request.user.username])
            row11 = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute('select rollno from student, guide, preferences where id = preferences.guide_id and rollno = preferences.student_roll and id=%s and allocated_flag=0;', [request.user.username])
            row21 = cursor.fetchall()
        row22 = [y for y in[x for x in row11]]
        row33 = [y for y in[x for x in row21]]
        row41 = [{'Student Name':row22[i][1], 'Roll Number':row22[i][0], 'CGPA':row22[i][2], 'Ideas':row22[i][3], 'Allocation Flag':row22[i][4], 'Department':row22[i][5], 'Interest':row22[i][6], 'Past Project Topic':row22[i][7]} for i in range(len(row22))]
        row31 = [{'Roll Number':row33[i][0]} for i in range(len(row33))]
        return render(request, 'project_management/showstudentinfo.html', {'data':"Select less choices",'data1':row31, 'data2':row41})

    for i in row3:
        a = request.POST.get('choice'+i)
        if(a=="Lock"):
            with connection.cursor() as cursor:
                cursor.execute('update student set allocated_flag=2 where rollno=%s;',[i])
                cursor.execute('insert into supervisor values(%s, %s, "F");',[request.user.username, i])
    with connection.cursor() as cursor:
        cursor.execute('update guide set seats_left=%s where id=%s;',[int(row1[0])-count,request.user.username])
    return render(request, 'project_management/employeelogin.html', {'data':"Changed Allocation"})

def assignproject(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select student_roll from supervisor where guide_id=%s', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/assignproject.html', {'data1':row2})

def assignedproject(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from supervisor where guide_id=%s and student_roll=%s;', [request.user.username, request.POST['roll']])
        r=cursor.fetchall()
    if(r[0][0]==0):
        with connection.cursor() as cursor:
            cursor.execute('select student_roll from supervisor where guide_id=%s', [request.user.username])
            row = cursor.fetchall()
        row2 = [y for x in row for y in x]
        return render(request, 'project_management/assignproject.html', {'data':"Select correct students", 'data1':row2})

    with connection.cursor() as cursor:
        cursor.execute('insert into project(topic, credits) values(%s, %s);', [request.POST['topic'], request.POST['credits']])
    with connection.cursor() as cursor:
        cursor.execute('select max(id) from project;')
        r1=cursor.fetchall()
    r2=[y for y in[x for x in r1]]
    pid=int(r2[0][0])
    with connection.cursor() as cursor:
        cursor.execute('update student set proj_id=%s where rollno=%s;',[pid, request.POST['roll']])
    with connection.cursor() as cursor:
        cursor.execute('select student_roll from supervisor where guide_id=%s', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/assignproject.html', {'data':"Assigned the Project", 'data1':row2})     

def fillproject(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select proj_id from supervisor, student, project where project.id=proj_id and guide_id=%s and student_roll=rollno', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    print datetime.date.today()
    print "faf"
    print datetime.datetime.now().date()
    return render(request, 'project_management/fillproject.html', {'data1':row2, 'd':str(datetime.date.today())})

def filledproject(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from supervisor, student where student_roll = rollno and guide_id=%s and proj_id=%s', [request.user.username, request.POST['project_id']])
        r=cursor.fetchall()
    if(r[0][0]==0):
        with connection.cursor() as cursor:
            cursor.execute('select proj_id from supervisor, student, project where project.id=proj_id and guide_id=%s and student_roll=rollno', [request.user.username])
            row = cursor.fetchall()
        row2 = [y for x in row for y in x]
        return render(request, 'project_management/fillproject.html', {'data':"Enter supervising project IDs only", 'data1':row2, 'd':str(datetime.date.today())})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from proj_guide where guide_id=%s and project_id=%s;',[request.user.username, request.POST['project_id']])
        r=cursor.fetchall()
    if(r[0][0]!=0):
        with connection.cursor() as cursor:
            cursor.execute('update proj_guide set guide_id=%s, checkpoint=%s, deadline=%s where project_id=%s;', [request.user.username, request.POST['checkpoint'], request.POST['deadline'], request.POST['project_id']])
        with connection.cursor() as cursor:
            cursor.execute('select proj_id from supervisor, student, project where project.id=proj_id and guide_id=%s and student_roll=rollno', [request.user.username])
            row = cursor.fetchall()
        print datetime.date.today()
        row2 = [y for x in row for y in x]
        return render(request, 'project_management/fillproject.html', {'data':"Updated the Project", 'data1':row2, 'd':str(datetime.date.today())})
    with connection.cursor() as cursor:
        cursor.execute('insert into proj_guide values(%s, %s, %s, %s);', [request.user.username, request.POST['project_id'], request.POST['checkpoint'], request.POST['deadline']])
    with connection.cursor() as cursor:
        cursor.execute('select proj_id from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
        row = cursor.fetchall()
    print datetime.date.today()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/fillproject.html', {'data':"Filled the Project", 'data1':row2, 'd':str(datetime.date.today())}) 

def assigngrades(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select rollno from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/assigngrades.html', {'data1':row2})

def assignedgrades(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from supervisor, student where guide_id=%s and student_roll=rollno and rollno=%s;', [request.user.username, request.POST['roll']])
        r=cursor.fetchall()
    if(r[0][0]==0):
        with connection.cursor() as cursor:
            cursor.execute('select rollno from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
            row = cursor.fetchall()
        row2 = [y for x in row for y in x]
        return render(request, 'project_management/assigngrades.html', {'data':"Only select correct students", 'data1':row2})
    with connection.cursor() as cursor:
        cursor.execute('update supervisor set grade=%s where guide_id=%s and student_roll=%s;', [request.POST['grade'], request.user.username, request.POST['roll']])
    with connection.cursor() as cursor:
        cursor.execute('select rollno from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/assigngrades.html', {'data':"Assigned the grades", 'data1':row2})

def attend(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select rollno from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/attend.html', {'data1':row2, 'd':str(datetime.date.today())})

def attenddone(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from supervisor where guide_id=%s and student_roll=%s;', [request.user.username, request.POST['roll']])
        r=cursor.fetchall()
    if(r[0][0]==0):
        with connection.cursor() as cursor:
            cursor.execute('select rollno from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
            row = cursor.fetchall()
        row2 = [y for x in row for y in x]
        return render(request, 'project_management/attend.html', {'data':"Enter correct students", 'data1':row2, 'd':str(datetime.date.today())})
    with connection.cursor() as cursor:
        cursor.execute('select attendance from student, supervisor where student_roll=%s;',[request.POST['roll']])
        row11 = cursor.fetchall()
    row21 = [y for x in row11 for y in x]
    with connection.cursor() as cursor:
        cursor.execute('update student set attendance=%s, next_meet=%s where rollno=%s;', [row21[0]+int(request.POST['attendance']), request.POST['meet'], request.POST['roll']])
    with connection.cursor() as cursor:
        cursor.execute('select rollno from supervisor, student where guide_id=%s and student_roll=rollno', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/attend.html', {'data':"Done", 'data1':row2, 'd':str(datetime.date.today())})

def panelsignup(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    return render(request, 'project_management/addpanel.html')

def createpanel(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    count = 0
    for i in range(7):
        if(len(request.POST['m'+str(i+1)])>0):
            count = count + 1
    with connection.cursor() as cursor:
        cursor.execute('insert into panel(cardinality, stage, password) values(%s, %s, "abc")', [count, request.POST['stage']])
    with connection.cursor() as cursor:
        cursor.execute('select max(id) from panel;');
        r=cursor.fetchall()
    r2=[y for y in[x for x in r]]
    pid=int(r2[0][0])
    print pid
    for i in range(7):
        if(len(request.POST['m'+str(i+1)])>0):
            with connection.cursor() as cursor:
                cursor.execute('insert into member values(%s, %s)', [request.POST['m'+str(i+1)], pid])
    return render(request, 'project_management/admin.html', {'data':"Created Panel"})

def adddoc(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select proj_id from student where rollno=%s;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/adddoc.html', {'data1':row2})

def addeddoc(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from project where id=%s;', [request.POST['pid']])
        r=cursor.fetchall()
    if r[0][0]==0:
        return render(request, 'project_management/adddoc.html', {'data':"Enter existing project ID"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from student where rollno=%s and proj_id=%s;', [request.user.username, request.POST['pid']])
        r=cursor.fetchall()
    if r[0][0]==0:
        return render(request, 'project_management/adddoc.html', {'data':"Enter assigned project ID"})
    with connection.cursor() as cursor:
        cursor.execute('insert into documents(location, type, proj_id, student_roll) values(%s, %s, %s, %s);', [request.POST['location'], request.POST['type'], request.POST['pid'], request.user.username])
    with connection.cursor() as cursor:
        cursor.execute('select proj_id from student where rollno=%s;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/adddoc.html', {'data':"Added document details successfully", 'data1':row2})

def seesen(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        userlike = request.user.username[0:2]+"%"
        cursor.execute('select student.name, topic, location, guide.name from student, supervisor, project, guide, documents where rollno not like %s and rollno=supervisor.student_roll and student.proj_id=project.id and documents.proj_id=project.id and guide.id=supervisor.guide_id;', [userlike])
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    print row2[0][0]
    print type(row2)
    row3 = [{'Student Name':row2[i][0], 'Project Topic':row2[i][1], 'Document Location':row2[i][2], 'Guide Name':row2[i][3]} for i in range(len(row2))]
    return render(request, 'project_management/showseniors.html', {'data1':row3})

def assignpanel(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select name, guide_id, panel_id from member, guide where guide_id=id;')
        row=cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row3 = [{'Guide Name':row2[i][0], 'Guide ID':row2[i][1], 'Panel ID':row2[i][2]} for i in range(len(row2))]
    with connection.cursor() as cursor:
        cursor.execute('select id from panel;')
        row=cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row4 = [{'Panel ID':row2[i][0]} for i in range(len(row2))]
    with connection.cursor() as cursor:
        cursor.execute('select id from project;')
        row=cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row5 = [{'Project ID':row2[i][0]} for i in range(len(row2))]
    return render(request, 'project_management/assignpanel.html', {'data2':row4, 'data3':row3, 'data4':row5})


def assignedpanel(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from panel, project where panel.id=%s and project.id=%s;', [request.POST['pid'], request.POST['prid']])
        r = cursor.fetchall()
    if(r[0][0]==0):
        with connection.cursor() as cursor:
            cursor.execute('select name, guide_id, panel_id from member, guide where guide_id=id;')
            row=cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row3 = [{'Guide Name':row2[i][0], 'Guide ID':row2[i][1], 'Panel ID':row2[i][2]} for i in range(len(row2))]
        with connection.cursor() as cursor:
            cursor.execute('select id from panel;')
            row=cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row4 = [{'Panel ID':row2[i][0]} for i in range(len(row2))]
        with connection.cursor() as cursor:
            cursor.execute('select id from project;')
            row=cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row5 = [{'Project ID':row2[i][0]} for i in range(len(row2))]
        return render(request, 'project_management/assignpanel.html', {'data':"Panel or Project does not exist", 'data2':row4, 'data3':row3, 'data4':row5})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from panel_proj where project_id=%s and panel_id=%s;',[request.POST['prid'], request.POST['pid']])
        r = cursor.fetchall()
    if(r[0][0]!=0):
        with connection.cursor() as cursor:
            cursor.execute('select name, guide_id, panel_id from member, guide where guide_id=id;')
            row=cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row3 = [{'Guide Name':row2[i][0], 'Guide ID':row2[i][1], 'Panel ID':row2[i][2]} for i in range(len(row2))]
        with connection.cursor() as cursor:
            cursor.execute('select id from panel;')
            row=cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row4 = [{'Panel ID':row2[i][0]} for i in range(len(row2))]
        with connection.cursor() as cursor:
            cursor.execute('select id from project;')
            row=cursor.fetchall()
        row2 = [y for y in[x for x in row]]
        row5 = [{'Project ID':row2[i][0]} for i in range(len(row2))]
        return render(request, 'project_management/assignpanel.html', {'data':"Panel already assigned", 'data2':row4, 'data3':row3, 'data4':row5})
    with connection.cursor() as cursor:
        cursor.execute('insert into panel_proj values(%s, %s, "F");',[request.POST['prid'], request.POST['pid']])
    return render(request, 'project_management/admin.html', {'data':"Assigned the panel"})

def assignedpanelgrades(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/adminlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('update panel_proj set grade = %s where panel_id=%s and project_id=%s;',[request.POST['grade'], request.POST['pid'], request.POST['prid']])
    return render(request, 'project_management/admin.html', {'data':"Assigned the grades"})

def markcheckpoint(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    return render(request, 'project_management/markcheckpoint.html')

def markedcheckpoint(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    a = request.POST.get('cp')
    with connection.cursor() as cursor:
        cursor.execute('update proj_guide set checkpoint=%s where project_id in (select id from project, student where id = proj_id and rollno=%s);', [a, request.user.username])
    return render(request, 'project_management/markcheckpoint.html', {'data':"Updated the checkpoint"})

def changecheckpoint(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select project_id from proj_guide where guide_id=%s;', [request.user.username])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    return render(request, 'project_management/changecheckpoint.html', {'data1':row1})

def changedcheckpoint(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from proj_guide where guide_id=%s and project_id=%s;', [request.user.username, request.POST['pid']])
        r=cursor.fetchall()
    if(r[0][0]==0):
        with connection.cursor() as cursor:
            cursor.execute('select project_id from proj_guide where guide_id=%s;', [request.user.username])
            row = cursor.fetchall()
        row1 = [y for x in row for y in x]
        return render(request, 'project_management/changecheckpoint.html', {'data':"Enter supervising project IDs only", 'data1':row1})
    a = request.POST.get('cp')
    with connection.cursor() as cursor:
        cursor.execute('update proj_guide set checkpoint=%s where guide_id=%s and project_id=%s;', [a, request.user.username, request.POST['pid']])
    with connection.cursor() as cursor:
        cursor.execute('select project_id from proj_guide where guide_id=%s;', [request.user.username])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    return render(request, 'project_management/changecheckpoint.html', {'data':"Changed the checkpoint", 'data1':row1}) 

def seeprojectdetails(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select guide.name, guide.id, attendance, next_meet, topic, credits, checkpoint, deadline, student.proj_id from supervisor, guide, student, project, proj_guide where student.proj_id = project.id and proj_guide.guide_id=guide.id and proj_guide.project_id=project.id and rollno=%s and supervisor.student_roll=rollno and guide.id = supervisor.guide_id;',[request.user.username])
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row3 = [{'Professor Name':row2[i][0], 'Professor ID':row2[i][1], 'Attendance':row2[i][2], 'Next Meet':row2[i][3], 'Project Topic':row2[i][4], 'Credits':row2[i][5], 'Checkpoint':row2[i][6], 'Deadline':row2[i][7], 'Project ID':row2[i][8]} for i in range(len(row2))]
    with connection.cursor() as cursor:
        cursor.execute('select student.proj_id, type, location, documents.id from student, documents where student.proj_id = documents.proj_id and rollno=%s;',[request.user.username])
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row4 = [{'Project ID':row2[i][0], 'Type':row2[i][1], 'Location':row2[i][2], 'Document ID':row2[i][3]} for i in range(len(row2))]
    return render(request, 'project_management/showprojectinfo.html', {'data1':row3, 'data2':row4})

def projectdetailsemployee(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select student.name, rollno, attendance, next_meet, topic, credits, checkpoint, deadline, grade, project.id from supervisor, guide, student, project, proj_guide where student.proj_id = project.id and proj_guide.guide_id=guide.id and proj_guide.project_id=project.id and guide.id=%s and supervisor.student_roll=rollno and guide.id = supervisor.guide_id;',[request.user.username])
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row3 = [{'Student Name':row2[i][0], 'Student Roll Number':row2[i][1], 'Attendance':row2[i][2], 'Next Meet':row2[i][3], 'Project Topic':row2[i][4], 'Credits':row2[i][5], 'Checkpoint':row2[i][6], 'Deadline':row2[i][7], 'Grade':row2[i][8], 'Project ID':row2[i][9]} for i in range(len(row2))]
    with connection.cursor() as cursor:
        cursor.execute('select student.name, rollno, student.proj_id, type, location, documents.id from supervisor, student, documents where student.proj_id = documents.proj_id and supervisor.guide_id=%s and supervisor.student_roll=rollno;',[request.user.username])
        row = cursor.fetchall()
    row2 = [y for y in[x for x in row]]
    row4 = [{'Student Name':row2[i][0], 'Student Roll Number':row2[i][1], 'Project ID':row2[i][2], 'Type':row2[i][3], 'Location':row2[i][4], 'Document ID':row2[i][5]} for i in range(len(row2))]
    return render(request, 'project_management/showprojectinfoemployee.html', {'data1':row3, 'data2':row4})

def finalgradesstudent(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select grade from supervisor, student where rollno=supervisor.student_roll and rollno=%s;', [request.user.username])
        row = cursor.fetchall()
    row1 = [y for x in row for y in x]
    with connection.cursor() as cursor:
        cursor.execute('select grade from panel_proj, student where proj_id=project_id and rollno=%s;', [request.user.username])
        row2 = cursor.fetchall()
    row3 = [y for x in row2 for y in x]
    d = {'A':10, 'A-':9, 'B':8, 'B-':7, 'C':6, 'C-':5, 'D':4, 'D-':3, 'E':2, 'E-':1, 'F':0}
    print row1
    print row3
    for i in range(len(row3)):
        print (int(d[row3[i]])!=0 or int(d[row1[0]])!=0)
        if(abs(d[row3[i]]-d[row1[0]])<=2 and (int(d[row3[i]])!=0 or int(d[row1[0]])!=0)):
            ans = (d[row3[i]]+d[row1[0]])/2
            print d[row3[i]]
            print d[row1[0]]
            print ans
            return render(request, 'project_management/showfinalgradesstudent.html', {'data1':ans})
    return render(request, 'project_management/showfinalgradesstudent.html', {'data1':"Not yet finalized"})

def updateprojects(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select project_topic from past_projects, student where rollno=%s and rollno=student_roll;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updatepastprojects.html', {'data1':row2})

def updateinterests(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select interest_area from stud_interest, student where rollno=%s and rollno=student_roll;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updateinterests.html', {'data1':row2})

def updatedprojects(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('insert into past_projects values(%s, %s);', [request.user.username, request.POST['project']])
    with connection.cursor() as cursor:
        cursor.execute('select project_topic from past_projects, student where rollno=%s and rollno=student_roll;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updatepastprojects.html', {'data1':row2})

def updatedinterests(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/studentlogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('insert into stud_interest values(%s, %s);', [request.user.username, request.POST['interest']])
    with connection.cursor() as cursor:
        cursor.execute('select interest_area from stud_interest, student where rollno=%s and rollno=student_roll;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updateinterests.html', {'data1':row2})

def updatepub(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select publication from guide_pub, guide where id=%s and id=guide_pub.guide_id;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updatepub.html', {'data1':row2})

def updateinterestsguide(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('select interest_area from guide_interest, guide where id=%s and id=guide_interest.guide_id;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updateinterestguide.html', {'data1':row2})

def updatedpub(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('insert into guide_pub values(%s, %s);', [request.user.username, request.POST['pub']])
    with connection.cursor() as cursor:
        cursor.execute('select publication from guide_pub, guide where id=%s and id=guide_pub.guide_id;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updatepub.html', {'data1':row2})

def updatedinterestsguide(request):
    if not request.user.is_authenticated:
        return render(request, 'project_management/employeelogin.html', {'data':"Login again"})
    with connection.cursor() as cursor:
        cursor.execute('insert into guide_interest values(%s, %s);', [request.user.username, request.POST['interest']])
    with connection.cursor() as cursor:
        cursor.execute('select interest_area from guide_interest, guide where id=%s and id=guide_interest.guide_id;', [request.user.username])
        row = cursor.fetchall()
    row2 = [y for x in row for y in x]
    return render(request, 'project_management/updateinterestguide.html', {'data1':row2})

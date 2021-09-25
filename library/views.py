from django.shortcuts import render,redirect
from django.http import Http404
from .models import *
from django.contrib.auth import login,logout,authenticate
import datetime
import s
# Create your views here.
def Home(request):
    return render(request, 'index.html')
def Add_book(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    error3=False
    data=Book.objects.all()

    if request.method=="POST":
        b = request.POST['book']
        i = request.POST['isbn']
        a = request.POST['author']
        c = request.POST['category']
        q = request.POST['quantity']
        Book.objects.create(book_name=b, author=a, isbn=i, category=c,quantity=q)
        error3=True
        d={'error3':error3,'data':data}
        return render(request,'bookview.html',d)

    return render(request,'AddBook.html')
def viewbook(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data=Book.objects.all()
    d={'data':data}
    return render(request,'bookview.html',d)
def Adminlogin(request):
    error=""
    if request.method=="POST":
        u=request.POST['username']
        p=request.POST['password']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d={'error':error}
    return render(request,'admin.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    bookcount=Book.objects.all().count()
    studentcount = Studentinfo.objects.all().count()
    d = {'bookcount':bookcount,'studentcount':studentcount}
    return render(request,'admin_home.html',d)



def Issue_Book(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    error=False
    data= Studentinfo.objects.all()
    data1=Book.objects.all()
    if request.method=="POST":

        bo = request.POST['book']
        e= request.POST['enroll']
        i= request.POST['isbn']
        tday=datetime.date.today()
        tdelta=datetime.timedelta(days=30)
        ex=tday+tdelta
        stu=Studentinfo.objects.filter(rollNo=e).first()
        book1 = Book.objects.filter(book_name=bo, isbn=i).first()
        Student.objects.create(studentinfo=stu,book=book1,issue_date=tday, expiry_date=ex)
        book1.quantity-=1
        book1.save()
        return redirect('viewissue')
        error=True
    d={'error':error,'studentinfo':data,'book':data1}
    return render(request,'issuebook.html',d)


def Signup_student(request):
    error=False
    error1=False
    if request.method == "POST":
        f=request.POST['firstname']
        l=request.POST['lastname']
        b=request.POST['branch']
        g=request.POST['email']
        u=request.POST['username']
        p=request.POST['password']
        e=request.POST['enroll']
        user = User.objects.filter(username = u)
        if user:
            error= True
        else:
            us = User.objects.create_user(username = u,password=p, first_name=f,last_name=l,email=g)
            Studentinfo.objects.create(user=us,rollNo=e,branch=b)
            error1=True
    d = {"error":error,'error1':error1}
    return render(request,'Signupstudent.html',d)

def Student_login(request):
    error=""
    if request.method=="POST":
        u=request.POST['username']
        p=request.POST['password']
        user=authenticate(request,username=u,password=p)
        if user:
            login(request,user)
            error = "no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'studentlogin.html',d)

def ViewOrder(request):
    if not request.user.is_authenticated:
        return redirect('studentlogin')
    data=Studentinfo.objects.filter(user=request.user.id).first()
    order1 = Student.objects.filter(studentinfo=data)
    d = {'data1':order1}
    return render(request,'orderview.html',d)

def Viewissue(request):
    if not request.user.is_authenticated:
        return redirect('studentlogin')
    order1 = Student.objects.all()
    d = {'data1':order1}
    return render(request,'viewissue.html',d)

def returnbook(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data1=Student.objects.get(id=pid)
    book = data1.book.id
    data = Book.objects.get(id=book)
    data1.delete()
    data.quantity+=1
    data.save()
    return redirect('viewissue')


def Fine(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginstudent')
    error=False
    data = Student.objects.get(id=pid)
    tday = datetime.date.today()
    d1 =  data.expiry_date
    f1 = 0
    d2 = 0
    if tday > d1:
        total_day = tday - d1
        f1 = int(str(total_day)[:-14]) * 5
        d2 = int(str(total_day)[:-14])
    else:
        f1=0
        d2=0
        error=True
    d={'fine':f1,'late':d2,'error':error}
    return render(request,'fineview.html',d)

def Fine2(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginstudent')
    error=False
    order1=Studentinfo.objects.filter(user=request.user.id).first()
    data = Student.objects.filter(studentinfo=order1,id=pid).first()
    tday = datetime.date.today()
    mon1 =  data.expiry_date.month
    d1 =  data.expiry_date.day
    f1=0
    d2=0
    if  mon1 == tday.month:
        if d1 < tday.day:
            d2=tday.day-d1
            f1=d2*5
            error=True
        else:
            pass
    elif  mon1 < tday.month:
        m2=tday.month-mon1
        d3=(30*m2)+tday.day
        d2=d3-d1
        f1=d2*5
        error=True

    else:
        f1=0
        d2=0
        error=True
    d={'fine':f1,'late':d2,'error':error}
    return render(request,'fine2.html',d)

def Logout(request):
    logout(request)
    return redirect('home')
def viewprofile(request,pid):
    if not request.user.is_authenticated:
        return redirect('studentlogin')
    user=User.objects.get(id=pid)
    data=Studentinfo.objects.filter(user=user).first()
    d={'data':data}
    return render(request,'viewprofile.html',d)
def edit(request,pid):
    if not request.user.is_authenticated:
        return redirect('studentlogin')
    error = ""
    user=User.objects.get(id=pid)
    data1=Studentinfo.objects.filter(user=user).get()
    if request.method == "POST":
        b=request.POST['branch']
        e=request.POST['enroll']
        f=request.POST['fname']
        l=request.POST['lname']
        data1.user.first_name=f
        data1.user.last_name=l
        data1.branch=b
        data1.rollNo=e
        try:
            data1.user.save()
            data1.save()
            error = "no"
        except:
            error = "yes"
    d = {'data':data1,'error':error}
    return render(request,'editprofile.html',d)

def edit_book(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    error=False
    data1=Book.objects.get(id=pid)
    if request.method == "POST":
        i=request.POST['isbn']
        b=request.POST['book']
        a=request.POST['author']
        q=request.POST['quantity']
        c=request.POST['cat']
        data1.isbn=i
        data1.book_name=b
        data1.category=c
        data1.quantity=q
        data1.author=a
        data1.save()
        error=True

    d = {'error':error,'data':data1}
    return render(request,'editbook.html',d)

def bookdelete(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data2=Book.objects.all()

    error1=False
    data = Book.objects.get(id=pid)
    data.delete()
    error1=True
    d = {'error1':error1,'data':data2}
    return render(request,'bookview.html',d)
def viewstudent(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    order1 = Studentinfo.objects.all()
    d = {'data1':order1}
    return render(request,'viewstudent.html',d)
def editstudent(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    error = ""
    data1=Studentinfo.objects.get(id=pid)
    if request.method == "POST":
        b=request.POST['branch']
        e=request.POST['enroll']
        f=request.POST['fname']
        l=request.POST['lname']
        data1.user.first_name=f
        data1.user.last_name=l
        data1.branch=b
        data1.rollNo=e
        try:
            data1.user.save()
            data1.save()
            error = "no"
        except:
            error="yes"
    d = {'data':data1,'error':error}
    return render(request,'editstudent.html',d)

def deletestudent(request,pid):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    error1=False
    data2=Studentinfo.objects.get(id=pid)
    data2.delete()
    return redirect('viewstudent')
    error1=True
    d = {'error1':error1,'data':data2}
    return render(request,'viewstudent.html',d)
def Registerstudent(request):
    error=False
    if request.method == "POST":
        f=request.POST['firstname']
        l=request.POST['lastname']
        b=request.POST['branch']
        g=request.POST['email']
        u=request.POST['username']
        p=request.POST['password']
        e=request.POST['enroll']
        user = User.objects.filter(username = u)
        if user:
            error= True
        else:
            us = User.objects.create_user(username = u,password=p, first_name=f,last_name=l )
            Studentinfo.objects.create(user=us,rollNo=e,branch=b)
            return redirect('viewstudent')
    d = {"error":error}
    return render(request,'registerstudent.html',d)
def searchbook(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data=Book.objects.all()
    d={'data':data}
    return render(request,'studentbooksearch.html',d)
def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    data = Book.objects.all()
    d = {'data': data}
    return render(request, 'placeorder.html', d)











from django.shortcuts import  render
from . import  pool
from django.contrib import auth

def AdminLogin(request):
    return render(request,"AdminLogin.html",{"msg":""})
def AdminChkLogin(request):
    adminemail=request.POST['adminemail']
    password=request.POST['password']
    query="select * from adminlogin where adminemailid='{0}' and password='{1}'".format(adminemail,password)
    db, cmd = pool.connection()
    cmd.execute(query)
    row=cmd.fetchone()
    if(row):
        request.session["ADMIN"]=row
        return render(request,"DashBoard.html", {'row':row})
    else:
        return render(request, "AdminLogin.html", {"msg": "Invalid Admin ID / Password"})

def AdminLogout(request):
    auth.logout(request)
    return render(request, "AdminLogin.html", {'msg': ''})



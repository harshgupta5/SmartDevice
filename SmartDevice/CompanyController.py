from django.shortcuts import render
from .import pool
from django.contrib import auth
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def CompanyInterface(request):
    try:
        row = request.session['ADMIN']
        return render(request, "CompanyInterface.html", {'msg': ''})
    except:
        return render(request, "AdminLogin.html", {'msg': ''})


@xframe_options_exempt
def SubmitRecord(request):
    try:
        companyname = request.POST['companyname']
        contactperson = request.POST['contactperson']
        mobilenumber = request.POST['mobilenumber']
        emailaddress = request.POST['emailaddress']
        location = request.POST['location']
        companyaddress = request.POST['companyaddress']
        state = request.POST['state']
        city = request.POST['city']
        zipcode= request.POST['zipcode']
        logo = request.FILES['companylogo']
        password = request.POST['password']
        db,cmd=pool.connection()
        q = "insert into companies(companyname,contactperson,contactpersonmobileno,location,address,state,city,zipcode,email,password,logo) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(
        companyname, contactperson, mobilenumber, location, companyaddress, state, city, zipcode,emailaddress,password,logo.name)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        F=open("E:/SmartDevice/assets/"+logo.name,"wb")
        for chunk in logo.chunks():
            F.write(chunk)
        F.close()

        return render(request, "CompanyInterface.html", {'msg': 'Record Submitted Successfully'})

    except Exception as e:
        print(e)
        return render(request, "CompanyInterface.html", {'msg': 'Server Error Failed to Submit Record'})
@xframe_options_exempt
def ListAllCompanies(request):
    try:
        row = request.session['ADMIN']
        db, cmd = pool.connection()
        query = "Select C . *,(select S.statename from states S where S.stateid=C.state) as statename,(select CT.cityname from cities CT where CT.cityid=C.city) as cityname  from companies C"
        cmd.execute(query)
        rows=cmd.fetchall()
        print(rows)
        return render(request,"AllCompanies.html",{'data': rows})
    except Exception as e:
        return render(request, "AllCompanies.html", {'data': []})

@xframe_options_exempt
def DisplayByCompanyId(request):
    try:
        cid=request.GET['cid']
        db, cmd = pool.connection()
        query = "Select C . *,(select S.statename from states S where S.stateid=C.state) as statename,(select CT.cityname from cities CT where CT.cityid=C.city) as cityname  from companies C where C.companyid={0}".format(cid)
        cmd.execute(query)
        row=cmd.fetchone()
        return render(request,"DisplayByCompanyId.html",{'data': row})
    except Exception as e:
        return render(request, "DisplayByCompanyId.html", {'data': []})
@xframe_options_exempt
def EditDeleteCompanyRecord(request):
    btn=request.GET['btn']
    if(btn=='Edit'):
     try:
        cid=request.GET['companyid']
        companyname = request.GET['companyname']
        contactperson = request.GET['contactperson']
        mobilenumber = request.GET['mobilenumber']
        emailaddress = request.GET['emailaddress']
        location = request.GET['location']
        companyaddress = request.GET['companyaddress']
        state = request.GET['state']
        city = request.GET['city']
        zipcode = request.GET['zipcode']
        password = request.GET['password']
        db, cmd = pool.connection()
        query="update companies set companyname='{0}',contactperson='{1}',contactpersonmobileno='{2}',email='{3}',location='{4}',address='{5}',state={6},city={7},zipcode='{8}',password='{9}' where companyid='{10}'".format(
            companyname, contactperson, mobilenumber, emailaddress, location, companyaddress, state, city, zipcode,
            password,cid)
        cmd.execute(query)
        db.commit()
        db.close()

        return ListAllCompanies(request)
     except Exception as e:
        print("error:",e)
        return ListAllCompanies(request)
    elif(btn=='Delete'):
        cid = request.GET['companyid']
        query="delete from companies where companyid={0}".format(cid)
        db, cmd = pool.connection()
        cmd.execute(query)
        db.commit()
        db.close()
        return ListAllCompanies(request)

def DisplayPictureCompany(request):
    cid = request.GET['cid']
    pic = request.GET['pic']
    return render(request, "DisplayPictureCompany.html", {"data": [cid, pic]})

def EditCompanyLogo(request):
    logo = request.FILES['companylogo']
    cid = request.POST['cid']
    db, cmd = pool.connection()
    query = "update companies set logo='{0}' where companyid='{1}'".format(logo.name, cid)
    print(query)
    cmd.execute(query)
    db.commit()
    db.close()
    F = open("E:/smartdevice/assets/" + logo.name, "wb")
    for chunk in logo.chunks():
        F.write(chunk)
    F.close()
    return ListAllCompanies(request)

def CompanyAdminLogin(request):
    return render(request,"CompanyAdminLogin.html",{"msg":""})
def CompanyAdminChkLogin(request):
    adminemail=request.POST['adminemail']
    password=request.POST['password']
    query="select * from companies where (email='{0}' or companyid='{1}') and password='{2}'".format(adminemail,adminemail,password)
    db, cmd = pool.connection()
    cmd.execute(query)
    row=cmd.fetchone()
    if(row):
        request.session["COMPANY"] = row
        return render(request,"CompanyDashBoard.html", {'row':row})
    else:
        return render(request, "CompanyAdminLogin.html", {"msg": "Invalid Admin ID / Password"})
def CompanyAdminLogout(request):
    auth.logout(request)
    return render(request, "CompanyAdminLogin.html", {"msg": ""})





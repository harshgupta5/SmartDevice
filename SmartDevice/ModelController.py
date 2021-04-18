from django.shortcuts import render
from .import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def ModelInterface(request):
    try:
        row = request.session["COMPANY"]
        return render(request,'ModelInterface.html',{'companyid':row[0]})
    except:
        return render(request, "CompanyAdminLogin.html", {"msg": ""})
def SubmitRecord3(request):
    try:
        companyid = request.POST['companyid']
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        modelname = request.POST['modelname']
        description = request.POST['description']
        db, cmd = pool.connection()
        q = "insert into models (companyid,categoryid,subcategoryid,modelname,modeldescription) values ('{0}','{1}','{2}','{3}','{4}')".format(companyid,categoryid,subcategoryid, modelname,description)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "ModelInterface.html", {'msg': 'Record Submitted Successfully'})

    except Exception as e:
        print(e)
        return render(request, "ModelInterface.html", {'msg': 'Server Error Failed to Submit Record'})
@xframe_options_exempt
def ListAllModel(request):
    try:
        row = request.session["COMPANY"]
        db, cmd = pool.connection()
        query ="select * from models"
        cmd.execute(query)
        rows=cmd.fetchall()
        print(rows)
        return render(request,"AllModel.html",{'data': rows})
    except Exception as e:
        return render(request, "CompanyAdminLogin.html", {'data': []})
def DisplayByModelID(request):
    try:
        modelid=request.GET['modelid']
        db,cmd=pool.connection()
        query="select * from models where modelid={0}".format(modelid)
        cmd.execute(query)
        row=cmd.fetchone()
        return render(request,"DisplayByModelId.html",{"data":row})
    except Exception as e:
        return render(request, "DisplayByModelId.html", {"data": []})
def EditDeleteModelRecord(request):
    try:
        modelid = request.GET['modelid']
        companyid = request.POST['companyid']
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        modelname = request.POST['modelname']
        description = request.POST['description']
        db, cmd = pool.connection()
        query = "update models set companyid='{0}',categoryid='{1}',subcategoryid='{2}',modelname='{3}',modeldescription='{4}' where modelid='{5}'".format(companyid,categoryid,subcategoryid,modelname,description,modelid)
        cmd.execute(query)
        print(query)
        db.commit()
        db.close()
        return ListAllModel(request)

    except Exception as e:
        return ListAllModel(request)

def fetchmodels(request):
    try:
        subcategoryid=request.GET['subcategoryid']
        db,cmd=pool.connection()
        cmd.execute("select * from models where subcategoryid={0}".format(subcategoryid))
        rows=cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        return JsonResponse(rows,safe=False)



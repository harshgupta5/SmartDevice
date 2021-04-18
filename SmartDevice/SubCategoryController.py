from django.shortcuts import render
from django.http import JsonResponse
from .import pool
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def SubCategoryInterface(request):
    try:
        row = request.session["COMPANY"]
        return render(request,'SubCategoryInterface.html',{'companyid':row[0]})
    except:
        return render(request, "CompanyAdminLogin.html", {"msg": ""})
@xframe_options_exempt
def SubmitRecord2(request):
    try:
        companyid = request.POST['companyid']
        categoryid = request.POST['categoryid']
        subcategoryname = request.POST['subcategoryname']
        description = request.POST['description']
        icon= request.FILES['icon']
        db, cmd = pool.connection()
        q = "insert into subcategory (companyid,categoryid,subcategoryname,description,icon) values ('{0}','{1}','{2}','{3}','{4}')".format(companyid,categoryid, subcategoryname,description,icon)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        F = open("E:/SmartDevice/assets/" + icon.name, "wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        return render(request, "SubCategoryInterface.html", {'msg': 'Record Submitted Successfully'})

    except Exception as e:
        print(e)
        return render(request, "SubCategoryInterface.html", {'msg': 'Server Error Failed to Submit Record'})
@xframe_options_exempt
def ListAllSubCategory(request):
    try:
        row = request.session["COMPANY"]
        db, cmd = pool.connection()
        query ="select * from subcategory"
        cmd.execute(query)
        rows=cmd.fetchall()
        print(rows)
        return render(request,"AllSubCategory.html",{'data': rows})
    except Exception as e:
        return render(request, "CompanyAdminLogin.html", {'data': []})


def DisplayBySubCategoryID(request):
    try:
        subcategoryid=request.GET['subcategoryid']
        db,cmd=pool.connection()
        query="select * from subcategory where subcategoryid={0}".format(subcategoryid)
        cmd.execute(query)
        row=cmd.fetchone()
        return render(request,"DisplayBySubCategoryId.html",{"data":row})
    except Exception as e:
        return render(request, "DisplayBySubCategoryId.html", {"data": []})
def EditDeleteSubCategoryRecord(request):
    btn = request.GET['btn']
    if (btn == 'Edit'):
     try:
        subcategoryid = request.GET['subcategoryid']
        companyid = request.GET['companyid']
        categoryid = request.GET['categoryid']
        subcategoryname = request.GET['subcategoryname']
        description = request.GET['description']
        db, cmd = pool.connection()
        query="update subcategory set companyid='{0}',categoryid='{1}',subcategoryname='{2}',description='{3}' where subcategoryid='{4}'".format(companyid,categoryid,subcategoryname,description,subcategoryid)
        cmd.execute(query)
        db.commit()
        db.close()
        return ListAllSubCategory(request)

     except Exception as e:
        return ListAllSubCategory(request)
    elif (btn == 'Delete'):
        subcategoryid = request.GET['subcategoryid']
        query = "delete from subcategory where subcategoryid={0}".format(subcategoryid)
        db, cmd = pool.connection()
        cmd.execute(query)
        db.commit()
        db.close()
        return ListAllSubCategory(request)
def DisplayPictureSubCategory(request):
    subcategoryid = request.GET['subcategoryid']
    pic = request.GET['pic']
    return render(request,"DisplayPictureSubCategory.html",{"data":[subcategoryid,pic]})
def EditSubCategoryLogo(request):
    icon = request.FILES['icon']
    subcategoryid = request.POST['subcategoryid']
    db,cmd=pool.connection()
    query = "update subcategory set icon='{0}' where subcategoryid='{1}'".format(icon.name,subcategoryid)
    cmd.execute(query)
    db.commit()
    db.close()
    F = open("E:/SmartDevice/assets/" + icon.name, "wb")
    for chunk in icon.chunks():
        F.write(chunk)
    F.close()
    return ListAllSubCategory(request)

# def FetchSubCategories(request):
#   try:
#     row = request.session["COMPANY"]
#     categoryid=request.GET['categoryid']
#     companyid=row[0]
#     db,cmd=pool.connection()
#     print("select * from subcategory where categoryid={0} and companyid={1}".format(categoryid,companyid))
#     cmd.execute("select * from subcategory where categoryid={0} and companyid={1}".format(categoryid,companyid))
#     rows=cmd.fetchall()
#     return JsonResponse(rows,safe=False)
#   except Exception as e:
#       return JsonResponse([], safe=False)

def FetchSubCategories(request):
  try:
    categoryid=request.GET['categoryid']
    db,cmd=pool.connection()
    cmd.execute("select * from subcategory where categoryid={0}".format(categoryid))
    rows=cmd.fetchall()
    return JsonResponse(rows,safe=False)
  except Exception as e:
      return JsonResponse([], safe=False)

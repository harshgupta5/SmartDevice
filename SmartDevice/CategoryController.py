from django.shortcuts import render
from .import pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def CategoryInterface(request):
    try:
        row = request.session["COMPANY"]
        return render(request,'CategoryInterface.html',{'companyid':row[0]})
    except:
        return render(request, "CompanyAdminLogin.html", {"msg": ""})
@xframe_options_exempt
def SubmitRecord1(request):
    try:
        companyid = request.POST['companyid']
        categoryname = request.POST['categoryname']
        icon= request.FILES['icon']
        db, cmd = pool.connection()
        q="insert into category (companyid,categoryname,icon) values ('{0}','{1}','{2}')".format(companyid,categoryname,icon)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        F = open("E:/SmartDevice/assets/" + icon.name, "wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        return render(request, "CategoryInterface.html", {'msg': 'Record Submitted Successfully'})

    except Exception as e:
        print(e)
        return render(request, "CategoryInterface.html", {'msg': 'Server Error Failed to Submit Record'})
@xframe_options_exempt
def ListAllCategories(request):
    try:
        row = request.session["COMPANY"]
        db, cmd = pool.connection()
        query = "select * from category"
        cmd.execute(query)
        rows=cmd.fetchall()
        print(rows)
        return render(request,"AllCategory.html",{'data': rows})
    except Exception as e:
        return render(request, "CompanyAdminLogin.html", {'data': []})
@xframe_options_exempt
def DisplayByCategoryID(request):
    try:
        categoryid=request.GET['categoryid']
        db,cmd=pool.connection()
        query="select * from category where categoryid={0}".format(categoryid)
        cmd.execute(query)
        row=cmd.fetchone()
        return render(request,"DisplayByCategoryId.html",{"data":row})
    except Exception as e:
        return render(request, "DisplayByCategoryId.html", {"data": []})

@xframe_options_exempt
def EditDeleteCategoryRecord(request):
    btn=request.GET['btn']
    if(btn=='Edit'):
        try:
            categoryid=request.GET['categoryid']
            companyid = request.GET['companyid']
            categoryname = request.GET['categoryname']
            db,cmd=pool.connection()
            query=" update category set companyid='{0}',categoryname='{1}' where categoryid='{2}' " .format(companyid,categoryname,categoryid)
            cmd.execute(query)
            db.commit()
            db.close()
            return ListAllCategories(request)
        except Exception as e:
            return  ListAllCategories(request)
    elif(btn=='Delete'):
        categoryid = request.GET['categoryid']
        query="delete from category where categoryid={0}".format(categoryid)
        db,cmd=pool.connection()
        cmd.execute(query)
        db.commit()
        db.close()
        return ListAllCategories(request)
def DisplayPictureCategory(request):
    categoryid = request.GET['categoryid']
    pic=request.GET['pic']
    return render(request,"DisplayPictureCategory.html",{"data":[categoryid,pic]})
def EditCategoryLogo(request):
    icon = request.FILES['icon']
    categoryid = request.POST['categoryid']
    db,cmd=pool.connection()
    query = "update category set icon='{0}' where categoryid='{1}'".format(icon.name, categoryid)
    cmd.execute(query)
    db.commit()
    db.close()
    F = open("E:/SmartDevice/assets/" + icon.name, "wb")
    for chunk in icon.chunks():
        F.write(chunk)
    F.close()
    return ListAllCategories(request)
def FetchCategories(request):
  try:
    db,cmd=pool.connection()
    cmd.execute("select * from category")
    rows=cmd.fetchall()
    return JsonResponse(rows,safe=False)
  except Exception as e:
      return JsonResponse([], safe=False)








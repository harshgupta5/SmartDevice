from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from .import pool
@xframe_options_exempt
def ProductInterface(request):
    try:
        row = request.session["COMPANY"]
        return render(request,"productinterface.html",{'companyid':row[0]})
    except:
        return render(request, "CompanyAdminLogin.html", {"msg": ""})
@xframe_options_exempt
def submitproduct(request):
    try:
        companyid=request.POST['companyid']
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        modelid = request.POST['modelid']
        productname=request.POST['productname']
        productprice=request.POST['productprice']
        mfgdate = request.POST['mfgdate']
        productpicture = request.FILES['productpicture']
        db,cmd=pool.connection()
        q="insert into products (companyid,categoryid,subcategoryid,modelid,productname,productprice,mfgdate,productpicture)values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(companyid,categoryid,subcategoryid,modelid,productname,productprice,mfgdate,productpicture.name)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        F = open("e:/smartdevice/assets/" + productpicture.name, "wb")
        for chunk in productpicture.chunks():
            F.write(chunk)
        F.close()
        return render(request,"productinterface.html",{'msg':"Record Submitted"})
    except Exception as e:

        print(e)
        return render(request, "productinterface.html", {'msg': "Server Error"})
@xframe_options_exempt
def Listallproducts(request):
    try:
        row = request.session["COMPANY"]
        db,cmd=pool.connection()
        q="select * from products"
        cmd.execute(q)
        rows=cmd.fetchall()
        return render(request,"allproducts.html",{"data":rows})
    except:
        return render(request, "allproducts.html", {"data": []})
@xframe_options_exempt
def displaybyproductid(request):
    try:
        cid=request.GET['cid']
        db,cmd=pool.connection()
        q="Select * from products where productid='{0}'".format(cid)
        cmd.execute(q)
        row=cmd.fetchone()
        return render(request,"displaybyproductid.html",{"data":row})
    except Exception as e:
        print('error:',e)
        return render(request, "displaybyproductid.html", {"data": []})
@xframe_options_exempt
def editdeleteproductrecord(request):
    btn=request.GET['btn']
    if(btn=='Edit'):

     try:
         cid=request.GET['productid']
         companyid = request.GET['companyid']
         categoryid = request.GET['categoryid']
         subcategoryid = request.GET['subcategoryid']
         modelid = request.GET['modelid']
         productname = request.GET['productname']
         productprice = request.GET['productprice']
         mfgdate = request.GET['mfgdate']


         db, cmd = pool.connection()
         query="update  products set companyid='{0}', categoryid='{1}' , subcategoryid='{2}',modelid='{3}',productname='{4}',productprice='{5}',mfgdate='{6}' where productid='{7}'".format(companyid,categoryid,subcategoryid,modelid,productname,productprice,mfgdate,cid)



         print(query)
         cmd.execute(query)
         db.commit()
         db.close()

         return Listallproducts(request)
     except Exception as e:
        print('ERROR:',e)

        return Listallproducts(request)


    elif(btn=='Delete'):
        cid = request.GET['productid']
        query="delete from products where productid='{0}'".format(cid)
        db, cmd = pool.connection()
        cmd.execute(query)
        db.commit()
        db.close()
        return Listallproducts(request)
@xframe_options_exempt
def displayproductpicture(request):
    cid=request.GET['cid']
    pic=request.GET['pic']
    return render(request, "displayproductpicture.html", {"data": [cid,pic]})

@xframe_options_exempt
def editproductpicture(request):
    productpicture= request.FILES['productpicture']
    cid= request.POST['cid']
    db, cmd = pool.connection()
    query = "update products set productpicture='{0}' where productid='{1}'".format(productpicture.name,cid)
    print(query)
    cmd.execute(query)
    db.commit()
    db.close()
    F = open("e:/smartdevice/assets/ " + productpicture.name, "wb")
    for chunk in productpicture.chunks():
        F.write(chunk)
    F.close()
    return Listallproducts(request)
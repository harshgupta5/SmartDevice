from django.shortcuts import  render
from django.views.decorators.clickjacking import xframe_options_exempt
from . import  pool
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
import time
@xframe_options_exempt
def Index(request):
    return render(request,"ClientView/index.html",{'msg':''})
@xframe_options_exempt
def UserRegistration(request):
    row = request.session["COMPANY"]
    print(row)
    return render(request, "ClientView/registration.html", {'msg': '', 'companyid': row[0]})
    #return render(request,"ClientView/registration.html",{'msg':''})



@xframe_options_exempt
def SubmitRecordCustomer(request):
    try:
        customermobile=request.POST['customermobile']
        customeremailid=request.POST['customeremailid']
        name=request.POST['name']
        companyid=request.POST['companyid']
        invoiceno=request.POST['invoiceno']
        productid=request.POST['productid']
        password=request.POST['password']
        db,cmd=pool.connection()
        q = "insert into customer(customermobile,customeremailid,name,companyid,invoiceno,password,productid) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(customermobile,customeremailid,name,companyid,invoiceno,password,productid)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "ClientView/registration.html", {'msg': 'Record Submitted Successfully'})
    except Exception as e:
        print(e)
        return render(request, "ClientView/registration.html", {'msg': 'Server Error Failed to Submit Record'})

@xframe_options_exempt
def UserLogin(request):
    return render(request, "ClientView/login.html", {'msg': ''})
def UserChkLogin(request):
 try:
    customermobile=request.POST['customermobile']
    password=request.POST['password']
    query="select * from customer where customermobile='{0}' and password='{1}'".format(customermobile,password)
    db, cmd = pool.connection()
    cmd.execute(query)
    row=cmd.fetchone()
    if (row):
        request.session['USER'] = row
        return UsersCategories(request)
    else:
        return render(request, "ClientView/login.html", {"msg": ""})
 except Exception as e:
      print(e)
      return render(request, "ClientView/login.html", {"msg": ""})

@xframe_options_exempt
def UsersCategories(request):
    try:
        row=request.session['USER']
        db, cmd = pool.connection()
        cmd.execute("select * from category where companyid={0}".format(row[3]))
        rows = cmd.fetchall()
        return render(request, "ClientView/categories.html",{'rows':rows})
    except Exception as e:
        return render(request, "ClientView/categories.html", {'rows':[]})
@xframe_options_exempt
def DisplaySubCategoryByCategoryId(request):
      try:
          cid = request.GET['cid']
          db, cmd = pool.connection()
          query = "select * from subcategory where categoryid={0}".format(cid)
          print(query)
          cmd.execute(query)
          rows = cmd.fetchall()
          return render(request, "ClientView/CompanySubcategories.html", {"rows": rows})
      except Exception as e:
          return render(request, "ClientView/CompanySubcategories.html", {"rows": []})
@xframe_options_exempt
def DisplayProductsBySubCategoryId(request):
      try:
          sid = request.GET['sid']
          db, cmd = pool.connection()
          row=request.session['USER']
          query = "select * from products where  subcategoryid={0} and productid={1}".format(sid,row[6])
          print(query)
          cmd.execute(query)
          rows = cmd.fetchall()
          if (len(rows) >= 1):
           request.session['USERPRODUCTS'] = rows
          return render(request, "ClientView/CompanyProducts.html", {"rows": rows})
      except Exception as e:
          return render(request, "ClientView/CompanyProducts.html", {"rows": []})

def OnAndOffDevice(request):
  btn=request.GET['btn']
  print("xxxxxxxxxxxxx",btn)
  ConnectToPubNub(btn)
  rows=request.session['USERPRODUCTS']
  return render(request, "ClientView/CompanyProducts.html", {"rows": rows})

def ConnectToPubNub(value):
    # Enter your PubNub Publish Key and use the Market Order Demo Subscribe Key
    pc = PNConfiguration()
    pc.subscribe_key = "sub-c-7dc5e4aa-2bdd-11eb-ae78-c6faad964e01"
    pc.publish_key = "pub-c-c21ee7d5-10c3-4667-9d1c-404c290c1250"
    pc.ssl = True
    pubnub = PubNub(pc)
    # Listen for Messages on the Market Order Channel
    channel = 'hp'

    def show(msg, stat):
        if (msg and stat):
            print(msg.timetoken, stat.status_code)
        else:
            print("Error", stat and stat.status_code)



        pubnub.publish().channel(channel).message(value).pn_async(show)
        time.sleep(2)



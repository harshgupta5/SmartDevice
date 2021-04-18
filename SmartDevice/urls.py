"""SmartDevice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import CompanyController
from .import StateCityController
from . import CategoryController
from . import SubCategoryController
from . import ModelController
from . import AdminController
from . import ProductController
from . import UserController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogout/',AdminController.AdminLogout),
    path('companyinterface/',CompanyController.CompanyInterface),
    path('submitrecord',CompanyController.SubmitRecord),
    path('fetchstates/',StateCityController.FetchStates),
    path('fetchcities/',StateCityController.FetchCities),
    path('listallcompanies/',CompanyController.ListAllCompanies),
    path('categoryinterface/',CategoryController.CategoryInterface),
    path('submitrecord1',CategoryController.SubmitRecord1),
    path('companyadminlogout/',CompanyController.CompanyAdminLogout),
    path('listallcategory/',CategoryController.ListAllCategories),
    path('subcategoryinterface/',SubCategoryController.SubCategoryInterface),
    path('submitrecord2',SubCategoryController.SubmitRecord2),
    path('listallsubcategory/',SubCategoryController.ListAllSubCategory),

    path('modelinterface/',ModelController.ModelInterface),
    path('listallmodel/',ModelController.ListAllModel),
    path('submitrecord3',ModelController.SubmitRecord3),
    path('displaybymodelid/',ModelController.DisplayByModelID),
    path('editdeletemodelrecord/',ModelController.EditDeleteModelRecord),

    path('displaybycompanyid/',CompanyController.DisplayByCompanyId),
    path('editdeletecompanyrecord/',CompanyController.EditDeleteCompanyRecord),
    path('displaypicturecompany/',CompanyController.DisplayPictureCompany),
    path('editcompanylogo',CompanyController.EditCompanyLogo),
    path('adminlogin/',AdminController.AdminLogin),
    path('adminchecklogin',AdminController.AdminChkLogin),
    path('displaybycategoryid/',CategoryController.DisplayByCategoryID),

    path('editdeletecategoryrecord/',CategoryController.EditDeleteCategoryRecord),
    path('displaypicturecategory/',CategoryController.DisplayPictureCategory),
    path('displaybysubcategoryid/',SubCategoryController.DisplayBySubCategoryID),

    path('editdeletesubcategoryrecord/',SubCategoryController.EditDeleteSubCategoryRecord),
    path('displaypicturesubcategory/',SubCategoryController.DisplayPictureSubCategory),

    path('editcategorylogo',CategoryController.EditCategoryLogo),
    path('editsubcategorylogo',SubCategoryController.EditSubCategoryLogo),

    path('companyadminlogin/',CompanyController.CompanyAdminLogin),
    path('companyadminchecklogin',CompanyController.CompanyAdminChkLogin),
    path('fetchcategory/',CategoryController.FetchCategories),

    path('fetchsubcategories/',SubCategoryController.FetchSubCategories),
    path('fetchmodels/',ModelController.fetchmodels),

#products
    path('productinterface/', ProductController.ProductInterface),
    path('submitproduct', ProductController.submitproduct),
    path('allproducts/', ProductController.Listallproducts),
    path('displaybyproductid/', ProductController.displaybyproductid),
    path('editdeleteproductrecord/', ProductController.editdeleteproductrecord),
    path('displayproductpicture/', ProductController.displayproductpicture),
    path('editproductpicture', ProductController.editproductpicture),



    path('userregistration/',UserController.UserRegistration),
    path('submitrecordcustomer',UserController.SubmitRecordCustomer),
    path('userlogin/',UserController.UserLogin),
    path('userchklogin',UserController.UserChkLogin),
    path('usercategory/',UserController.UsersCategories),
    path('userproductsubcategories/',UserController.DisplaySubCategoryByCategoryId),
    path('userproductlist/',UserController.DisplayProductsBySubCategoryId),
    path('index/',UserController.Index),
    path('onandoffdevice/',UserController.OnAndOffDevice),



]
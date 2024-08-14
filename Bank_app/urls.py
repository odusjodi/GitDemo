from django.urls import path
from . import views

#the url routing file linking paths to classes in the views.py file. It also provide an alternative name value to access the paths
urlpatterns = [
    path("register", views.UserClassCreation.as_view(), name="registeruser"),
    path("login", views.UserLogin.as_view(), name="loginuser"),
    path("logout", views.UserLogOut.as_view(), name="logoutuser"),
    path("customer", views.Customers.as_view(), name="customerview"),
    path("<int:id>", views.Customer_Edit.as_view(), name="customeredit"),
    path("del_<int:id_del>", views.Customer_Delete.as_view(), name="delete"),
    path("add<int:add_id>", views.Account_Add.as_view(), name="accountadd"),
    path("accview", views.Account_View.as_view(), name="accountview"),
    path("accedit<int:accid>", views.Account_Edit.as_view(), name="accountedit"),
    path("moneytransfer", views.Transfer.as_view(), name="transfer"),
    path("transview", views.Transaction_View.as_view(), name="transactionview"),
    path("index", views.Index.as_view(), name="indexpg"),
    path("adminpage", views.LoginAdmin.as_view(), name="adminpg"),
    
] 
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as log_Out
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from Bank_app.models import Account, TrackAccount, Transactions
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import secrets
from django.db.models import F
from datetime import date





#Class to validate data inputted in the registration and login page
class DataValidator:
    
    @staticmethod
    def validate(data_dict):
        for key, value in data_dict.items():
            if not value:
                return False
        return True
    
    @staticmethod
    def validateEqualPwd(data_dict):
        if data_dict['pwd1'] != data_dict['pwd2']:
                return False
        return True
    
 
 


#Class call to handle user registration; inherits from the View super class methods n properties
class UserClassCreation(View):
    
    #Handles all get requests - it displays the registration page to the user
    def get(get, request):
        return render(request, "Bank_app/user.html")
    
    #Handles all post request/actions initiated on the registration page
    def post(get, request):
        
        form_data = {'name': request.POST.get('fullname', ''), 
                    'username': request.POST.get('username', ''), 
                    'email': request.POST.get('email', ''), 
                    'pwd1': request.POST.get('pwd1', ''), 
                    'pwd2': request.POST.get('pwd2', '')
                    }
        if not DataValidator.validate(form_data):
            # Handle invalid form data, perhaps return an error response
            return render(request, "Bank_app/user.html", {"hasSuccess":False, "message": "Invalid form data"})
        try:
            user = User.objects.create_user(first_name=form_data['name'], 
                                            username=form_data['username'], 
                                            email=form_data['email'], 
                                            password=form_data['pwd1'])
            user.save()
            #to track account number creation
            TrackAccount(user_id=user.id, hasAccount="Reg").save()
        except Exception as e:
            print(f"Error try to save data {e}")
            return render(request, "Bank_app/user.html", {"hasSuccess":False, "message":"Username is not unique"})
        
        return render(request, "Bank_app/user.html", {"hasSuccess":True, "message":"User created"})




        
#This class handle login request from customer not admin; 
class UserLogin(View):
    
    #Renders  the login page to the customer
    def get(self, request):
        return render(request, "Bank_app/login.html")
    
    #handles submission requestion initiated from the login page
    def post(self, request):
        form_data = { 'username': request.POST.get('username', ''),'pwd1':request.POST.get('pwd1', '')}
        user = authenticate(request, username=form_data['username'], password=form_data['pwd1'])
        
        if user is not None:
            auth_login(request, user)
            to_id = User.objects.get(pk=request.user.id)
            
        
            customer_acc_details = Account.objects.get(aUser_id = to_id.id)
            return render(request, "Bank_app/index.html", 
                        {"customer_acc_details":customer_acc_details})
        else:
            return render(request, "Bank_app/login.html", 
                        {"hasSuccess":False, "message":"Invalid credentials "})
        
  
  
#Handles login request for admin staff  
class LoginAdmin(View):
    def get(self, request):
        return render(request, "Bank_app/login.html")
    
    def post(self, request):
        form_data = { 'username': request.POST.get('username', ''),'pwd1':request.POST.get('pwd1', '')}
        user = authenticate(request, username=form_data['username'], password=form_data['pwd1'])
        
        if user is not None:
            auth_login(request, user)
            return render(request, "Bank_app/index.html")
        else:
            return render(request, "Bank_app/login.html", 
                        {"hasSuccess":False, "message":"Invalid credentials "})
      
  
  
#Destroys the session created when logged on.   
class UserLogOut(View):
    def get(self, request):
        log_Out(request)
        print("logout true")
        return render(request, "Bank_app/thankyou.html")
    


#The staff is able to view all reigstered customers (users)
@method_decorator(login_required(login_url='adminpg'), name='dispatch')
class Customers(View):
    
    def get(self, request):
        #cust_accounts = Account.objects.select_related("aUser")
        #all_registered_customers = User.objects.all().exclude(is_superuser = True)  
        all_registered_customers = User.objects.select_related('userprofile').all().exclude(is_superuser = True)   
        return render(request, "Bank_app/customer.html", {"customers": all_registered_customers})



#The staff is able to edit the details of a customer (users)
@method_decorator(login_required(login_url='adminpg'), name='dispatch')   
class Customer_Edit(View):

#This return the edit customer details page when the staff clicks on the customer to edit   
    def get(self, request, id):  
        user_info = User.objects.get(pk=id) 
        return render(request, "Bank_app/customer_edit.html", {"user_info":user_info})
    
#To save the changes to the customer information, the block of code is executed   
    def post(self, request, id):
        user_info = User.objects.filter(pk=id).update(first_name=request.POST.get("fullname"), email=request.POST.get("email"))
        return render(request, "Bank_app/customer_edit.html", {"hasSuccess":"Details updated successfully"})
    



#Handles the deletion of customer eg, if it is apparent wrong data were used for registration
@method_decorator(login_required(login_url='adminpg'), name='dispatch')
class Customer_Delete(View):
    
#This block of code returned the details of the customer to be delete with a delete bottom
    def get(self, request, id_del):  
        userinfo = User.objects.get(pk=id_del) 
        return render(request, "Bank_app/customer_delete.html", {"user_info":userinfo})
    
#The block is called to notified the staff record was deleted
    def post(self, request, id_del):
        user_info = User.objects.filter(pk=id_del).delete()
        return render(request, "Bank_app/customer_delete.html", {"hasSuccess":"Record deleted successfully"})
 


    
#handles the addition of generated accounts to a User/Customer
@method_decorator(login_required(login_url='adminpg'), name='dispatch')
class Account_Add(View):
#
    def get(self, request, add_id):  
        cust_info = User.objects.all().get(id=add_id) 
        accountNos = secrets.randbelow(900000) + 100000
        newAccount = Account(
                aDate=date.today(),
                balance=00.00, 
                status=True, 
                accountNumber = accountNos,
                accountType="Savings", 
                accountCount=1, 
                aUser=cust_info)
        newAccount.save()
        #TrackAccount(user_id=cust_info.id, hasAccount=True).save()
        print('customer id--')
        print(cust_info.id)
        subTrack = TrackAccount.objects.all().get(user_id=cust_info.id)
        subTrack.hasAccount = "Act"
        subTrack.save()
        return render(request, "Bank_app/account_add.html", {"cust_info":cust_info,
                                                            "accountNo": accountNos})
  

  
        
#returns all the all generated that is stored in the database, SQLite 
@method_decorator(login_required(login_url='adminpg'), name='dispatch')      
class Account_View(View):
    def get(self, request):
        allaccounts = Account.objects.select_related('aUser__userprofile').all()
        return render(request, "Bank_app/account_view.html", {"allaccounts":allaccounts})
    
    def post(self, request):
        pass
 
 
    
#Handles the edit funationality  - to either Enable of Disable an account
@method_decorator(login_required(login_url='adminpg'), name='dispatch') 
class Account_Edit(View):
    
#Returns the detailed page to edited 
    def get(self, request, accid):
        account_to_edit = Account.objects.all().get(aUser=accid)
        return render(request, "Bank_app/account_status_edit.html", {"account_to_edit": account_to_edit})
        
#Code block handles the changes
    def post(self, request, accid):
        Account.objects.filter(aUser=request.POST.get('user_id_html','')).update(status=request.POST.get('account_status',''))
        s= request.POST.get('account_status','')
        return render(request, "Bank_app/account_status_edit.html", {"hasSuccess": "Status updated"})
  
  
    
#The Class handles transfer from one account to another.
#It does a varieties of checked to ensure account is enable and sufficient funds are available
#Subsequently the financial exchange is carried out and the activities are recorded in the 
#transaction table. this is used for statements
@method_decorator(login_required(login_url='loginuser'), name='dispatch')
class Transfer(View):
    def get(self, request):
        customer_acc_details = Account.objects.all().get(aUser_id = request.user.id)
        recipients_accounts = Account.objects.all().exclude(accountNumber = customer_acc_details.accountNumber)
        return render(request, "Bank_app/transfer.html", {"customer_acc_details": customer_acc_details,
                                                          "recipients_accounts": recipients_accounts})

    def post(self, request):
        amount = request.POST.get('amount','')
        account_nos = request.POST.get('recipient_account','')
        try:
            #check recipient account is valid and active
            recipient_details = Account.objects.get(accountNumber =account_nos, status = 1 )
        except Exception as e:
            print(f"there is an issue {e}")
            return render(request, "Bank_app/transfer.html", {"hasSuccess":False, 
                                                            "message": "Account # maybe wrong or inactive!"})
        
        try:
            #check sender(logged user) account is sufficiently funded and active
            sender_details = Account.objects.get(aUser_id = request.user.id, status = 1 )
        except Exception as e:
            print(f"there is an issue {e}")
            return render(request, "Bank_app/transfer.html", {"hasSuccess":False, 
                                                            "message": " Account maybe insufficiently funded or inactive!"})
        #check customer has sufficient balance
        if sender_details.balance > float(amount):
            customer_new_bal = sender_details.balance - float(amount)
            Account.objects.filter(aUser_id=request.user.id).update(balance=customer_new_bal)
            Account.objects.filter(accountNumber=account_nos).update(balance=F('balance') + float(amount))
            
            #write activities to Transaction table (SENDER)
            sender_decription = f"£{float(amount)} Debit trf to A/C{account_nos}"
            Transactions(tDate=date.today(), tDescription=sender_decription,tAccount=sender_details, tBalance=customer_new_bal ).save()
            
            #write activities to Transaction table (RECIPIENT)==============error for firt transanction
          
            recipient_decription = f"£{float(amount)} Credit trf frm A/C{recipient_details.accountNumber}"
            Transactions(tDate=date.today(), tDescription=recipient_decription, tBalance=recipient_details.balance, tAccount=recipient_details).save()
            print("tables were updated")
            
            return render(request, "Bank_app/transfer.html", {"hasSuccess":"Sent", 
                                                            "message": "Transfer successful!"})
        else:
            #do another
            return render(request, "Bank_app/transfer.html", {"hasSuccess":False, 
                                                            "message": "Insufficient funds!"})
        
        
        return render(request, "Bank_app/transfer.html")
    


#Handles all the display of financially activities done by a logged used. 
@method_decorator(login_required(login_url='loginuser'), name='dispatch')  
class Transaction_View(View):
    def get(self, request):
        accountInstance = Account.objects.all().get(aUser_id=request.user.id)
        transaction_stmnt = Transactions.objects.filter(tAccount_id = accountInstance.id).order_by('-tDate')
        return render(request, "Bank_app/statement.html", {"transaction_stmnt":transaction_stmnt})
    
    def post(self, request):
        pass
 
 
 
#On successful log on, a user is routed to the index.html page. the page is dynamic as what displays is dependent
#on if the user is a staff or a customer(user) 
@method_decorator(login_required(login_url='loginuser'), name='dispatch')  
class Index(View):
    def get(self, request):
        return render(request, "Bank_app/index.html")
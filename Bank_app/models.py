from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your data models. These classes automatically created data table in the SQLite server


#Accounts (details) actioned by the staff are store in the model, Account.
class Account(models.Model):
    aDate = models.DateTimeField()
    status = models.BooleanField(default=False)
    accountNumber = models.IntegerField()
    balance = models.FloatField()
    accountType = models.CharField(max_length=20)
    accountCount = models.IntegerField()
    aUser = models.ForeignKey(User, on_delete=models.CASCADE)
 
 
 #The model was created to track registered user with/without an account   

class TrackAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    hasAccount = models.CharField(max_length=12)
    
#the transaction model stores every cash transaction initiated by customers.
class Transactions(models.Model):
    tDate = models.DateField()
    tDescription = models.CharField(max_length=20)
    tBalance=models.FloatField()
    tAccount = models.ForeignKey(Account, on_delete=models.CASCADE)
    


#the User model (table) store detail of registered user. It's also
#used for authentication. The model comes by default on SQLite and appears in the SQLIte interface.
#The model can be alter from the model.py and via the shell.
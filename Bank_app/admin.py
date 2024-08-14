from django.contrib import admin
from .models import Account, TrackAccount, Transactions

admin.site.register(Account)
admin.site.register(TrackAccount)
admin.site.register(Transactions)


# Register your models here.

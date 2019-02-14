from django.db import models
from account.models import CustomerProfile,User,ParaProfile



class Cart(models.Model):
    client    =  models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True,blank=True)
    total     =  models.IntegerField(default=0)
    ordered   =  models.BooleanField(default=False)

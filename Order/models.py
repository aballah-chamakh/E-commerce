from django.db import models
from Cart.models import Cart
from account.models import ParaProfile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import date
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

## Create your models here.
class Order(models.Model):
    reference = models.CharField(max_length=255,blank=True,null=True)
    cart = models.OneToOneField(Cart,on_delete=models.CASCADE)
    para = models.ForeignKey(ParaProfile,on_delete=models.CASCADE,blank=True,null=True)
    shipping_address = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateField(auto_now_add=True,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    runing = models.BooleanField(default=True)
    shipped = models.BooleanField(default=False)
    delivered  =  models.BooleanField(default=False)
    

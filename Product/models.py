from django.db import models
from Cart.models import Cart
from account.models import ParaProfile
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Product(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    image       = models.ImageField()
    price       = models.IntegerField()

class ClientCustomProduct(models.Model):
    product        = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart           = models.ForeignKey(Cart,on_delete=models.CASCADE)
    count          = models.IntegerField(default=1)


class ParaCustomProduct(models.Model):
    para    = models.ForeignKey(ParaProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    count   = models.IntegerField(default=1)


@receiver(post_save, sender=ClientCustomProduct)
def calculate_cart_total(sender, instance, created, **kwargs):
    cart_obj = instance.cart
    products = cart_obj.clientcustomproduct_set.all()
    total = 0
    for product in products :
        total = total + (int(product.product.price) * int(product.count))
    cart_obj.total = total
    cart_obj.save()

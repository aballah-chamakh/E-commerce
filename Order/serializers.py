from rest_framework import serializers
from .models import Order
from Cart.serializers import CartSerializer
from Product.serializers import ProductSerializer
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
class OrderSerializer(serializers.ModelSerializer):
    cart_info   = serializers.SerializerMethodField('get_cart_obj_info',read_only=True)
    cart_total = serializers.IntegerField(source='cart.total')
    customer_username = serializers.CharField(source='cart.client.user.username',read_only=True)

    #time = serializers.DateTimeField(read_only=True)
    class Meta :
        model = Order
        fields = ['id','customer_username','reference','time','cart_info','cart_total','shipping_address','phone','runing','shipped','delivered']
    def get_cart_obj_info(self,order_obj):
        cart_obj = order_obj.cart
        serializer = CartSerializer(cart_obj,many=False,context={'request':self.context['request']})
        return serializer.data



class OrderListSerializer(serializers.ModelSerializer):
    #product_count = serializers.SerializerMethodField('get_order_products_count',read_only=True)
    cart_total = serializers.IntegerField(source='cart.total')
    customer_username = serializers.CharField(source='cart.client.user.username',read_only=True)
    para_username = serializers.CharField(source='para.user.username',read_only=True)


    class Meta :
        model = Order
        fields = ['id','para_username','customer_username','cart_total','shipping_address','phone','time','runing','shipped','delivered']
    def get_order_products_count(self,order_obj):
        count = 0
        products = order_obj.cart.clientcustomproduct_set.all()
        for product in products :
            count += product.count
        return count



@receiver(post_save, sender=Order)
def send_notification(sender, instance, created, **kwargs):
    if created :
        print('let us send a not ', instance.para.channel_name)
        channel_layer = get_channel_layer()
        serializer = OrderSideListSerializer(instance,many=False)
        order = serializer.data
        order['type'] = 'new_order'
        async_to_sync(channel_layer.send)(instance.para.channel_name,{
          'type':'notification.message',
          'text': order
        })

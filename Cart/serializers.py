from rest_framework import serializers
from Product.serializers import ClientCustomProductSerializer
from .models import Cart

class CartSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField('related_products')
    count    = serializers.SerializerMethodField('get_cart_count')
    #client_name = serializers.CharField(source='client.user.username')
    # client_id   = serializers.IntegerField(source='client.user.id')
    class Meta :
        model = Cart
        fields = ['id','products','total','count']

    def related_products(self,cart_obj):
        client_custom_prodcuts = cart_obj.clientcustomproduct_set.all()
        serializer = ClientCustomProductSerializer(client_custom_prodcuts,many=True,context={'request':self.context['request']})
        return serializer.data
    def get_cart_count(self,cart_obj):
        return cart_obj.clientcustomproduct_set.count()

class CartCountSerializer(serializers.ModelSerializer):
    count    = serializers.SerializerMethodField('get_cart_count')
    class Meta :
        model = Cart
        fields = ['count']
    def get_cart_count(self,cart_obj):
        products = cart_obj.clientcustomproduct_set.all()
        length = 0
        for product in products :
            length += product.count
        return length

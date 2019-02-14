from rest_framework import serializers
from .models import Product,ClientCustomProduct,ParaCustomProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = ['id','image','name','description','price']


class ClientCustomProductSerializer(serializers.ModelSerializer):

    cart_id      = serializers.IntegerField(source='cart.id')
    product      = serializers.SerializerMethodField('get_the_product')
    #user_name    = serializers.CharField(source='cart.client.user.username')
    #user_id      = serializers.IntegerField(source='cart.client.user.id')

    class Meta :
        model = ClientCustomProduct
        fields = ['id','product','cart_id','count']
    def get_the_product(self,custom_product_obj):
        serializer = ProductSerializer(custom_product_obj.product,many=False,context={'request':self.context['request']})
        return serializer.data




class ParaCustomProductSerializer(serializers.ModelSerializer):
    para_id = serializers.IntegerField(source='para.id')
    para_name = serializers.CharField(source='product.name')
    product_id = serializers.IntegerField(source='para.id')
    product_name = serializers.CharField(source='product.name')
    class Meta :
        models = ParaCustomProduct
        fields = ['id','para_id','para_name','product_id','product_name','count']

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Product,ClientCustomProduct
from .serializers import ProductSerializer,ClientCustomProductSerializer
from Cart.models import Cart
# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # still we need to review this func
    def get_queryset(self):
        search = self.request.GET.get('search')
        qs =  Product.objects.all()
        if search :
            qs = Product.objects.filter(name=search)
        return qs


class DeleteClientCustomProduct(generics.DestroyAPIView):
    queryset = ClientCustomProduct.objects.all()
    serializer_class = ClientCustomProductSerializer

class ClientCustomProductViewset(ModelViewSet):
    queryset = ClientCustomProduct.objects.all()
    serializer_class = ClientCustomProductSerializer
    @action(methods=['put'],detail=True)
    def increase_count(self,request,pk):
        custom_product_obj = self.get_object()
        custom_product_obj.count += 1
        custom_product_obj.save()
        return Response({'response':'product increased'},status=status.HTTP_200_OK)
    @action(methods=['put'],detail=True)
    def decrease_count(self,request,pk):
        custom_product_obj = self.get_object()
        custom_product_obj.count -= 1
        custom_product_obj.save()
        return Response({'response':'product increased'},status=status.HTTP_200_OK)
    @action(methods=['post'],detail=False)
    def add_product_to_cart(self,request):
        cart_id  = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        product_obj = Product.objects.get(id=product_id)
        cart_obj = None
        response = {'response':'product added'}
        if cart_id :
            cart_obj = Cart.objects.get(id=cart_id)
        else :
            cart_obj = Cart.objects.create()
            response['cart_id'] = cart_obj.id
        qs = cart_obj.clientcustomproduct_set.all().filter(product__id=product_obj.id)
        if qs :
            custom_product_obj = qs[0]
            custom_product_obj.count += 1
            custom_product_obj.save()
        else :
            ClientCustomProduct.objects.create(product=product_obj,cart=cart_obj)
        return Response({'response':response,'cart_id':cart_obj.id},status=status.HTTP_200_OK)

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Cart
from .serializers import CartSerializer,CartCountSerializer
from Product.models import ClientCustomProduct
from Order.models import Order
from account.models import ParaProfile

# Create your views here.


class CartViewset(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    def perform_create(self,serializer):
        serializer.save(client=self.request.user.customerprofile)


    # still we need to review this func
    @action(methods=['put'],detail=True)
    def set_product_qty(self,request,pk):
        cart_obj    = self.get_object()
        product_id  = request.data.get('product_id')
        product_qty = request.data.get('product_qty')
        product_obj = ClientCustomProduct.objects.get(id=product_id)
        product_obj.count = product_qty
        product_obj.save()
        return Response({'response':'qty updated'},status=status.HTTP_200_OK)

    # still we need to review this func
    @action(methods=['post'],detail=True)
    def order_cart(self,request,pk):
        shipping_address = request.data.get('shipping_address')
        phone = request.data.get('phone')
        para_id = request.data.get('para_id')
        # raise an erro if this data not available
        para_obj = ParaProfile.objects.get(id=para_id)
        cart_obj = self.get_object()
        cart_obj.ordered = True
        cart_obj.save()
        new_order = Order.objects.create(cart=cart_obj,shipping_address=shipping_address,
                                         phone=phone,para=para_obj)
        profile_obj = request.user.customerprofile
        new_cart = Cart.objects.create(client=profile_obj)
        return  Response({'cart_id':new_cart.id},status=status.HTTP_200_OK)


class CartCountView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCountSerializer

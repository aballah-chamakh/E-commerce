from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from Cart.models import Cart
from account.models import ParaProfile
from .serializers import OrderSerializer,OrderListSerializer
from Product.models import Product,ClientCustomProduct
from Product.serializers import ProductSerializer
import json

class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self,serializer):
        cart_id  = self.request.data.get('cart_id')
        para_id  = self.request.data.get('para_id')
        cart_obj = Cart.objects.get(id=cart_id)
        cart_obj.ordered = True
        cart_obj.save()
        para_obj = ParaProfile.objects.get(id=para_id)
        serializer.save(cart=cart_obj,para=para_obj)



    def list(self,request):
        profile = None
        orders = self.queryset



        if request.user.is_admin :
            orders = orders.order_by('-time')

        elif self.request.user.selling_point == False  :
            profile = self.request.user.customerprofile
            orders = orders.filter(cart__client=profile).order_by('-time')

        elif self.request.user.selling_point == True  :
            print('this is a para')
            profile = self.request.user.paraprofile
            orders = orders.filter(para=profile).order_by('-time')


        #orders = self.queryset.filter(cart__client=profile).order_by('-time')
        serializer = OrderListSerializer(orders,many=True)
        return Response({'order_list':serializer.data},status=status.HTTP_200_OK)
    @action(methods=['get'],detail=False)
    def last_order(self,request):
        orders = self.queryset.filter(cart__client=request.user.customerprofile,
                                            runing=True,shipped=False,delivered=False).distinct().order_by('-timestamp')

        serializer = OrderSerializer(orders[0],many=False,context={'request':request})
        #print(serializer.data)
        return Response({'last_order':serializer.data},status=status.HTTP_200_OK)
    @action(methods=['put',],detail=True)
    def set_shipped(self,request,pk):
        if request.user.selling_point == False :
            return Response({'response':'you can not do this action as customer'},status=status.HTTP_401_UNAUTHORIZED)
        order = self.get_object()
        state = self.request.data.get('state')
        order.shipped = state
        order.save()
        print('set order to shipped '+str(order.delivered))

        return Response({'response':'this order is shipped now'},status=status.HTTP_200_OK)
    @action(methods=['put',],detail=True)
    def set_delivered(self,request,pk):
        if request.user.selling_point == False :
            return Response({'response':'you can not do this action as customer'},status=status.HTTP_401_UNAUTHORIZED)

        order = self.get_object()
        state = self.request.data.get('state')
        order.delivered = state
        order.save()
        print('set order to delivered '+str(order.delivered))
        return Response({'response':'this order is delivered now'},status=status.HTTP_200_OK)

    @action(methods=['get'],detail=False)
    def order_analytics(self,request):
        products = Product.objects.all()
        orders = Order.objects.all().filter(para=request.user.paraprofile)
        all_ordered_products = ClientCustomProduct.objects.all().filter(cart__order__para=request.user.paraprofile)
        analytics_data = []
        # loop throught all our mproduct
        for product in products :
            # filter all ordered product comming to the para by unique product
            unique_ordered_products = all_ordered_products.filter(product=product)
            if len(unique_ordered_products) == 0  :
                continue
            count = 0
            for unique_ordered_product in unique_ordered_products :
                count += unique_ordered_product.count
            serializer = ProductSerializer(product,many=False)
            analytics_data.append({'product':serializer.data,'count':count})

        return Response({'analytics_data':analytics_data},status=status.HTTP_200_OK)

from rest_framework import routers
from django.urls import path
from django.conf.urls import include
from .views import CartViewset,CartCountView


router = routers.DefaultRouter()
router.register('cart',CartViewset)

urlpatterns = [
path('',include(router.urls)),
path('cart_count/<int:pk>/',CartCountView.as_view())
]

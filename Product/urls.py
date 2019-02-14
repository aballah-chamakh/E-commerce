from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import ProductViewSet,DeleteClientCustomProduct,ClientCustomProductViewset

router = routers.DefaultRouter()
router.register('product',ProductViewSet)
router.register('client_custom_product',ClientCustomProductViewset)

urlpatterns = [
path('',include(router.urls)),
path('custom_client_product/<int:pk>/delete/',DeleteClientCustomProduct.as_view())

]

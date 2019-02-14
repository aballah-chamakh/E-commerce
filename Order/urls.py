from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from .views import OrderViewset

router = routers.DefaultRouter()
router.register('order',OrderViewset)

urlpatterns = [
path('',include(router.urls))
]

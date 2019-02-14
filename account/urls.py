from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from .views import UserViewSet,ParaProfileViewSet,CustomerProfileViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('para', ParaProfileViewSet)
router.register('customer', CustomerProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),


]

from django.conf.urls import include
from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

from Product import urls as product_url
from Cart import urls as cart_urls
from Order import urls as order_urls
from account import urls as account_urls

urlpatterns = [
path('',include(product_url)),
path('',include(cart_urls)),
path('',include(order_urls)),
path('',include(account_urls)),
path('token/', obtain_jwt_token, name='token_obtain_pair'),
path('refresh_token/', refresh_jwt_token, name='refresh_jwt_token'),
]

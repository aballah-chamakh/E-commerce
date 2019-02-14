from rest_framework import permissions


class OrderPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = requets.user
        if user.selling_point :
            return obj.para = user.paraprofile
        else :
            return obj.cart.client == user.customerprofile

class CartPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = requets.user
        cart_obj = obj
        if cart_obj.client is None :
            return True 
        else :
            return cart_obj.client == requets.user.customerprofile

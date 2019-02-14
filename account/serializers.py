from rest_framework import serializers
from .models import Profile,CustomerProfile,ParaProfile
from Product.models import ParaCustomProduct
from Product.serializers import ParaCustomProductSerializer,ClientCustomProductSerializer
from Cart.serializers import CartSerializer
from Cart.models import   Cart
from Order.models import Order
from Order.serializers import OrderListSerializer
from .models import User,ParaProfile,CustomerProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True,required=True)
    address  = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta :
        model = User
        fields =('id','selling_point','username','email','password','address','phone')
    # def validate(self,data):
    #     email = data.get('email')
    #     qs = User.objects.filter(email=email)
    #     if qs :
    #         raise serializers.ValidationError('email already exist')
    #     pw1 = data.get('password')
    #     pw2 = data.pop('password2')
    #     # chech if the two password match
    #     if pw1 != pw2 :
    #         raise serializers.ValidationError('Passwords should match')
    #     return data
    def create(self,validated_data):
        username      = validated_data.get('username')
        email         = validated_data.get('email')
        password      = validated_data.get('password')
        address       = validated_data.get('address')
        phone         = validated_data.get('phone')
        selling_point = validated_data.get('selling_point')
        cart_id       = validated_data.get('cart_id')
        # create the user
        user_obj = User(username=username,email=email,selling_point=selling_point)
        user_obj.set_password(password) # to save the password in a hashed format
        user_obj.save()
        # attach to this user a parofile or a customer based on the selling point attribute
        profile = None
        if selling_point :
            profile = ParaProfile.objects.create(user=user_obj,address=address,phone=phone)
        else :
            profile = CustomerProfile.objects.create(user=user_obj,address=address,phone=phone)
        # attach to this user a cart if it's a customer and not a selling_point
        if cart_id and selling_point == False :
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.client = profile
            cart_obj.save()
        return user_obj





class CustomerProfileSerializer(serializers.ModelSerializer):
    #cart = serializers.SerializerMethodField('get_client_cart_products',read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)
    join_at = serializers.DateTimeField(source='user.created_at',read_only=True)
    revenue = serializers.SerializerMethodField('calc_revenue')
    orders = serializers.SerializerMethodField('get_related_orders')
    email = serializers.CharField(source='user.email',read_only=True)
    class Meta :
        model  = CustomerProfile
        fields = ['id','email','username','phone','revenue','image','address','join_at','orders']

    def get_client_cart_products(self,client_profile_obj):
        cart_obj = client_profile_obj.cart_set.all().get(ordered=False)
        serializer = CartSerializer(cart_obj,many=False)
        return serializer.data
    def get_related_orders(self,customer_obj):
        qs = Order.objects.filter(cart__client=customer_obj)
        serializer = OrderListSerializer(qs,many=True,context={'request':self.context['request']})
        return serializer.data
    def calc_revenue(self,obj):
        qs = Order.objects.filter(cart__client=obj,shipped=True)
        total = 0
        for order in qs :
            total =+ order.cart.total
        return total

class CustomerProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    join_at = serializers.DateTimeField(source='user.created_at',read_only=True)
    revenue = serializers.SerializerMethodField('calc_revenue')
    class Meta :
        model = CustomerProfile
        fields = ['id','username','phone','revenue','image','address','join_at']
    def calc_revenue(self,obj):
        qs = Order.objects.filter(cart__client=obj,shipped=True)
        total = 0
        for order in qs :
            total =+ order.cart.total
        return total





class ParaProfileSerializer(serializers.ModelSerializer):
    revenue = serializers.SerializerMethodField('calc_revenue',read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)
    orders = serializers.SerializerMethodField('get_related_orders')
    join_at = serializers.DateTimeField(source='user.created_at',read_only=True)
    email = serializers.CharField(source='user.email',read_only=True)

    class Meta :
        model =  ParaProfile
        fields = ['join_at','id','username','email','image','phone','address','revenue','orders']
    def calc_revenue(self,para_obj):
        qs = Order.objects.filter(para=para_obj,delivered=True)
        revenue = 0
        for order in qs :
            revenue += order.cart.total
        return revenue
    def get_related_orders(self,para_obj):
        qs = Order.objects.filter(para=para_obj)
        serializer = OrderListSerializer(qs,many=True,context={'request':self.context['request']})
        return serializer.data


class ParaProfileListSerializer(serializers.ModelSerializer):
    revenue = serializers.SerializerMethodField('calc_revenue',read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)
    class Meta :
        model =  ParaProfile
        fields = ['id','username','image','phone','address','revenue']
    def calc_revenue(self,para_obj):
        qs = Order.objects.filter(para=para_obj,delivered=True)
        revenue = 0
        for order in qs :
            revenue += order.cart.total
        return revenue



class SimpleUserSerializer(serializers.ModelSerializer):
    profile_id = serializers.SerializerMethodField('get_user_profile_id',read_only=True)
    cart_id = serializers.SerializerMethodField('get_user_cart_id')
    class Meta :
        model  = User
        fields = ('id','username','selling_point','profile_id','cart_id','is_admin')
    def get_user_profile_id(self,user_obj):
        if user_obj.selling_point:
            return user_obj.paraprofile.id
        return user_obj.customerprofile.id
    def get_user_cart_id(self,user_obj):
        if user_obj.selling_point :
            return None
        qs = user_obj.customerprofile.cart_set.all().filter(ordered=False)
        cart_obj = None
        if qs :
            cart_obj = qs[0]
        else:
            cart_obj = Cart.objects.create(client=user_obj.customerprofile)
        return cart_obj.id

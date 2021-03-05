from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from .push import send_notification,send_notification_store,send_notification_delivery_boy


User._meta.get_field('email')._unique = True


from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','image','phone','address','is_store','is_customer','is_deliveryBoy','latitude',\
            'longitude','push_token')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','image','phone','address','is_store','is_customer','is_deliveryBoy')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
         model=User
         fields=('username','password') 
    

class DeliveryBoySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = DeliveryBoy
        fields = ['user','id','status']

class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Store
        fields = ['id','user']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['user','id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    delivery_boy_detail = DeliveryBoySerializer(source='delivery_boy', read_only=True)
    store_detail = StoreSerializer(source='store', read_only=True)
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
    
    def create(self, validated_data):
        customer = validated_data['customer'].user
        stores = User.objects.filter(is_store=True)
        delivery_boys = DeliveryBoy.objects.filter(status="ACTIVE")
        print(stores)
        temp_store = send_notification_store(customer,self,stores)
        print("DElocery boys are: ",delivery_boys)
        delivery_boy = send_notification_delivery_boy(customer,self,temp_store,delivery_boys)
        store = temp_store
        print("Customer from serializer",customer)
        validated_data['store'] = Store.objects.get(user=store)
        validated_data['delivery_boy'] = DeliveryBoy.objects.get(user=delivery_boy)
        return Order.objects.create(**validated_data)

class OrderProductSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class DeliveryBoyNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoyNotifications
        fields = "__all__"

class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = "__all__"

# class CitySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     pincode = serializers.CharField(max_length=50)
#     lat = serializers.CharField(max_length=50)
#     lng = serializers.CharField(max_length=50)
#     owner_id = serializers.IntegerField()

#     def create(self,validated_data):
#         return City.objects.create(**validated_data)

#     def update(self,instance,validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.name = validated_data.get('name', instance.name)
#         instance.pincode = validated_data.get('pincode', instance.pincode)
#         instance.lat = validated_data.get('lat', instance.lat)
#         instance.lng = validated_data.get('lng', instance.lng)
#         instance.save()
#         return instance


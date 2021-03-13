from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .forms import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,serializers
from rest_framework import permissions
from rest_framework import status,filters
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.db.models import Q
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token



class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token 
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = AuthToken.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)



class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        login(request, user)
        print(request)
        return super(LoginView, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        UserSerializer2 = UserSerializer

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,

        }
        if UserSerializer is not None:
            data["user"] = UserSerializer2(
                request.user,
                context=self.get_context()
            ).data
            if data["user"]['is_store']:
                store = Store.objects.get(user=data['user']['id'])
                data["store"] = StoreSerializer(store).data
            if data["user"]['is_customer']:
                customer = Customer.objects.get(user=data['user']['id'])
                data["customer"] = CustomerSerializer(customer).data
            if data["user"]['is_deliveryBoy']:
                print("i am executed")
                deliveryBoy = DeliveryBoy.objects.get(user=data['user']['id'])
                data["deliveryBoy"] = DeliveryBoySerializer(deliveryBoy).data
        return data

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DeliveryBoyViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryBoySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = DeliveryBoy.objects.all()



class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Store.objects.all()

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Customer.objects.all()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.all().order_by('-id')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Order.objects.all().order_by('-id')
        customer = self.request.query_params.get('customer', None)
        deliveryBoy = self.request.query_params.get('deliveryBoy', None)
        status = self.request.query_params.get('status', None)
        store = self.request.query_params.get('store', None)
        exclude = self.request.query_params.get('exclude', None)
        if customer is not None:
            queryset = queryset.filter(customer=customer)
        if status is not None:
            queryset = queryset.filter(status=status)
        if store is not None:
            queryset = queryset.filter(store=store)
        if deliveryBoy is not None:
            queryset = queryset.filter(delivery_boy=deliveryBoy)
        if exclude is not None:
            print(exclude)
            queryset = queryset.exclude(status=exclude)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # print("The instance is ",instance)
        # print("Request data is ",request.data)
        if 'user_complete' in request.data:
            delivery_boy_complete = instance.delivery_boy_complete
            if request.data['user_complete'] == delivery_boy_complete:
                instance.status = "DELIVERED"    
        if 'delivery_boy_complete' in request.data:
            user_complete = instance.user_complete
            if request.data['delivery_boy_complete'] == user_complete:
                instance.status = "DELIVERED"
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class OrderProductViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = [permissions.AllowAny]
    queryset = OrderProduct.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OrderProduct.objects.all().order_by('-id')
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order_id=order_id)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductCategory.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ProductCategory.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            queryset = queryset.filter(order_id=order_id)
        return queryset

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subscription.objects.all()

class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = SubscriptionType.objects.all()

class BannerViewSet(viewsets.ModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Banner.objects.all()

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Notification.objects.all()

class DeliveryBoyNotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryBoyNotificationsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = DeliveryBoyNotifications.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = DeliveryBoyNotifications.objects.all().order_by('-id')
        deliveryBoy = self.request.query_params.get('deliveryBoy', None)
        exclude = self.request.query_params.get('exclude', None)
        if deliveryBoy is not None:
            queryset = queryset.filter(delivery_boy=deliveryBoy)
        if exclude is not None:
            queryset = queryset.exclude(status=exclude)
        return queryset

class ComplainViewSet(viewsets.ModelViewSet):
    serializer_class = ComplainSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Complain.objects.all()


# class CityAPI(generics.ListCreateAPIView):
#     queryset = City.objects.all()
#     serializer_class = CitySerializer


# class city_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = City.objects.all()
#     serializer_class = CitySerializer
#     permission_classes = [permissions.IsAuthenticated]

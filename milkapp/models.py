from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from .push import send_notification,send_notification_store,send_notification_delivery_boy
from django.utils import timezone

class User(AbstractUser):
    image = models.ImageField(height_field=None, width_field=None, max_length=None)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=11,blank=True,null=True)
    is_customer = models.BooleanField(default=False)
    is_store = models.BooleanField(default=False)
    is_deliveryBoy = models.BooleanField(default=False)
    push_token = models.CharField(max_length=200,default="")

    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            if self.is_customer:
                Customer.objects.create(user=self)
            elif self.is_store:
                Store.objects.create(user=self)
            elif self.is_deliveryBoy:
                DeliveryBoy.objects.create(user=self)

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(height_field=None, width_field=None, max_length=None)
    price = models.IntegerField()
    description = models.TextField()
    discount = models.IntegerField()
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    can_subscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Store(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class DeliveryBoy(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.CharField(default="ACTIVE",max_length=50)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(DeliveryBoy,on_delete=models.CASCADE,default=1)
    price = models.IntegerField(default=0)
    status = models.CharField(max_length=50,default="ACTIVE")
    created_at = models.DateTimeField(default=timezone.now)
    user_complete = models.BooleanField(default=False)
    delivery_boy_complete = models.BooleanField(default=False)

    # def save(self,*args,**kwargs):
    #     created = not self.pk
    #     customer = self.customer.user
    #     stores = User.objects.filter(is_store=True)
    #     delivery_boys = User.objects.filter(is_deliveryBoy=True)
    #     print(stores)
    #     temp_store = send_notification_store(customer,self,stores)
    #     print("DElocery boys are: ",delivery_boys)
    #     delivery_boy = send_notification_delivery_boy(customer,self,temp_store,delivery_boys)
    #     store = temp_store.id
    #     print(super().__dict__)
    #     super().store_id = store
    #     super().delivery_boy_id = delivery_boy
    #     #super().save(*args,**kwargs) # this is the creation of the order


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='Product')
    quantity = models.IntegerField(default=1)


class SubscriptionType(models.Model):
    name = models.CharField(max_length=200)
    interval = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField(default=1)
    timing = models.TimeField(auto_now=False, auto_now_add=False,default=timezone.now)
    price = models.IntegerField(default=0)
    status = models.CharField(max_length=50,default="Active")
    subscription = models.ForeignKey(SubscriptionType,on_delete=models.CASCADE, default=0)


class Banner(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    url = models.CharField(max_length=250,default="www.eazisols.com")

class Notification(models.Model):
    message = models.TextField()
    title = models.CharField(max_length=100)

    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        Users = User.objects.all()
        if created:
            for user in Users:
                if not user.push_token == "":
                    return send_notification(user.push_token,self.title,self.message)
            

    def __str__(self):
        return self.title

class Complain(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    query = models.TextField()
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class DeliveryBoyNotifications(models.Model):
    message = models.TextField()
    title = models.CharField(max_length=100)
    delivery_boy = models.ForeignKey(DeliveryBoy,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        boy = DeliveryBoy.objects.get(id=self.delivery_boy.id).user
        if created:
            if not boy.push_token == "":
                return send_notification(boy.push_token,self.title,self.message)

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(DeliveryBoy)
admin.site.register(Banner)
admin.site.register(Subscription)
admin.site.register(SubscriptionType)
admin.site.register(Notification)
admin.site.register(DeliveryBoyNotifications)
admin.site.register(Complain)



import string

from .push import send_notification_store
from .models import Subscription,Store,User

from celery import shared_task
from datetime import datetime, date




@shared_task
def my_task():
    queryset = Subscription.objects.all()
    stores = User.objects.filter(is_store=True)
    for order in queryset:
        x = datetime.now().time()
        duration = datetime.combine(date.min, x) - datetime.combine(date.min, order.timing)
        hours = duration.total_seconds() // 3600
        minutes = (duration.total_seconds()//60)%60
        if (hours==0 and (minutes<35 and minutes>30)):
            send_notification_store(order.customer.user,order,stores)
        print ("Minutes : ",minutes, hours)
        print(" I am being executedsdas")

from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer


from . import consumers
from . import restconsumers
from . import views

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/orders/', restconsumers.OrdersConsumer.as_asgi()),
    re_path(r'ws/deliveryboys/(?P<room_name>\w+)/$', consumers.DeliveryBoyLocationConsumer.as_asgi()),
    re_path(r'ws/deliveryboys-notifications/', restconsumers.DeliveryBoyNotificationsConsumer.as_asgi()),
]
from . import models
from . import serializers
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
    RetrieveModelMixin
)

class OrdersConsumer(    
    ListModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
    GenericAsyncAPIConsumer):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.AllowAny]

    async def accept(self, **kwargs):
        await super().accept(** kwargs)
        await self.model_change.subscribe()


    @model_observer(models.Order)
    async def model_change(self, message, action=None, **kwargs):

        await self.send_json({'data' : message,'action' : action})

    ''' If you want the data serializeded instead of pk '''
    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return serializers.OrderSerializer(instance).data


class DeliveryBoyNotificationsConsumer(    
    ListModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
    GenericAsyncAPIConsumer):
    queryset = models.DeliveryBoyNotifications.objects.all()
    serializer_class = serializers.DeliveryBoyNotificationsSerializer
    permission_classes = [permissions.AllowAny]

    async def accept(self, **kwargs):
        await super().accept(** kwargs)
        await self.model_change.subscribe()


    @model_observer(models.DeliveryBoyNotifications)
    async def model_change(self, message, action=None, **kwargs):
        print(message)
        await self.send_json({'data' : message,'action' : action})

    ''' If you want the data serializeded instead of pk '''
    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return serializers.DeliveryBoyNotificationsSerializer(instance).data

# class DeliveryBoyConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
#     queryset = models.DeliveryBoy.objects.all()
#     serializer_class = serializers.DeliveryBoy

#     async def accept(self, **kwargs):
#         await super().accept(** kwargs)
#         await self.model_change.subscribe()


#     @model_observer(models.User)
#     async def model_change(self, message, action=None, **kwargs):

#         await self.send_json({'data' : message,'action' : action})

#     ''' If you want the data serializeded instead of pk '''
#     @model_change.serializer
#     def model_serialize(self, instance, action, **kwargs):
#         return serializers.DeliveryBoySerializer(instance).data
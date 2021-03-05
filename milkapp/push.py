import requests 
import json
from .models import *
from .utils import calculate_distance
# defining the api-endpoint  

def send_notification(push_token,title,message):
    API_ENDPOINT = "https://exp.host/--/api/v2/push/send"
    data = {
    'to': push_token,
    'sound': 'default',
    'title': title,
    'body': message,
    }
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data) 
    print("Response is : ",r.json())
    # extracting response text  
    pastebin_url = r.text 
    print("The pastebin URL is:%s"%pastebin_url) 


def send_notification_store(Customer,order,stores):
    our_store = stores[0]
    distance = calculate_distance(Customer.latitude,Customer.longitude,our_store.latitude,our_store.longitude)
    for store in stores:
        temp = calculate_distance(Customer.latitude,Customer.longitude,store.latitude,store.longitude)
        if distance > temp:
            distance = temp
            our_store = store
    print(our_store.__dict__)
    push_token = our_store.push_token


    API_ENDPOINT = "https://exp.host/--/api/v2/push/send"
    data = {
    'to': push_token,
    'sound': 'default',
    'title': "title",
    'body': "message",
    }
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data) 
    print("Response is : ",r.json())
    # extracting response text  
    pastebin_url = r.text 
    return our_store

def send_notification_delivery_boy(Customer,order,our_store,riders):
    our_rider = riders[0].user
    distance = calculate_distance(our_rider.latitude,our_rider.longitude,our_store.latitude,our_store.longitude)
    for rider in riders:
        temp = calculate_distance(rider.user.latitude,rider.user.longitude,our_store.latitude,our_store.longitude)
        if distance > temp:
            distance = temp
            our_rider = rider
    print(our_store.__dict__)
    push_token = our_rider.push_token


    API_ENDPOINT = "https://exp.host/--/api/v2/push/send"
    data = {
    'to': push_token,
    'sound': 'default',
    'title': "title",
    'body': "message",
    }
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data) 
    print("Response is : ",r.json())
    # extracting response text  
    print("The selected rider is ",our_rider)
    return our_rider


# send_notification_store(User.objects.get(is_store=True),Order.objects.get(id=4))

# async def send_notification_delivery_boy(store,order):
#     d_boys = User.objects.get(is_deliveryBoy=True)
#     for boy in d_boys:
#         distance = await calculate_distance(store.latitude,store.longitude,boy.latitude,boy.longitude)


#     API_ENDPOINT = "https://exp.host/--/api/v2/push/send"
#     data = {
#     'to': push_token,
#     'sound': 'default',
#     'title': title,
#     'body': message,
#     }
#     # sending post request and saving response as response object 
#     r = requests.post(url = API_ENDPOINT, data = data) 
#     print("Response is : ",r.json())
#     # extracting response text  
#     pastebin_url = r.text 
#     print("The pastebin URL is:%s"%pastebin_url) 


# send_notification_delivery_boy(User.objects.get(is_store=True),Order.objects.get(id=4))


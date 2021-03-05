"""doodhwaley URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from milkapp import views
from rest_framework import routers
from milkapp import views
from rest_framework.urlpatterns import format_suffix_patterns
from knox.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'deliveryboy', views.DeliveryBoyViewSet)
router.register(r'store', views.StoreViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'order-product', views.OrderProductViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'product-category', views.ProductCategoryViewSet)
router.register(r'subscription', views.SubscriptionViewSet)
router.register(r'subscription-type', views.SubscriptionTypeViewSet)
router.register(r'banner', views.BannerViewSet)
router.register(r'user', views.UserList)
router.register(r'notification', views.NotificationViewSet)
router.register(r'deliveryboy-notifications', views.DeliveryBoyNotificationsViewSet)
router.register(r'complain', views.ComplainViewSet)


urlpatterns = [
    #path('api/auth/', include('knox.urls')),
    path('api/auth/login/', views.LoginView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('api/auth/logout/', LogoutView.as_view(), name='knox_logout'),
    path('api/', include(router.urls)),
    path('api/changePassword/', views.ChangePasswordView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



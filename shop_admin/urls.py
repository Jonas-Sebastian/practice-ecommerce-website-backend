from django.urls import path
from .views import ShopAdminAccountCreateView, ShopAdminLoginView

urlpatterns = [
    path('register/', ShopAdminAccountCreateView.as_view(), name='shop_admin_register'),
    path('login/', ShopAdminLoginView.as_view(), name='shop_admin_login'),
]

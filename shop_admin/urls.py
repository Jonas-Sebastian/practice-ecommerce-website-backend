from django.urls import path
from .views import (
    ShopAdminAccountCreateView,
    ShopAdminLoginView,
    ShopAdminAccountListView,
    ShopAdminAccountDetailView, 
)

urlpatterns = [
    path('register/', ShopAdminAccountCreateView.as_view(), name='shop_admin_register'),
    path('login/', ShopAdminLoginView.as_view(), name='shop_admin_login'),
    path('admin-users/', ShopAdminAccountListView.as_view(), name='shop_admin_list'),
    path('admin-users/<int:pk>/', ShopAdminAccountDetailView.as_view(), name='shop_admin_detail'),
]

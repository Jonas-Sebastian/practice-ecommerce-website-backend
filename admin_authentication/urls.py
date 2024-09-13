from django.urls import path
from .views import ShopAdminLoginView

urlpatterns = [
    path('login/', ShopAdminLoginView.as_view(), name='shop-admin-login'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<int:pk>/update-status/', OrderViewSet.as_view({'patch': 'update_status'}), name='order-update-status'),
    path('orders/<int:pk>/items/', OrderViewSet.as_view({'get': 'get_order_items'}), name='order-items'),
]
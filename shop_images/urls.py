from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeroImageViewSet

router = DefaultRouter()
router.register(r'hero-images', HeroImageViewSet)  # Register the viewset with the router

urlpatterns = [
    path('', include(router.urls)),
]
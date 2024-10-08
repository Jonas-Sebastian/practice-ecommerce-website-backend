from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/practice-shop/', include('practice_shop.urls')),
    path('api/shop-admin/', include('shop_admin.urls')),
    path('api/shop-images/', include('shop_images.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

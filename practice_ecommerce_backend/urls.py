from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/practice-shop/', include('practice_shop.urls')),
    path('api/shop-admin/', include('shop_admin.urls')),
    path('api/shop-images/', include('shop_images.urls')),
] 

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
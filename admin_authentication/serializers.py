from rest_framework import serializers
from .models import ShopAdminAccount

class ShopAdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAdminAccount
        fields = ('id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser')

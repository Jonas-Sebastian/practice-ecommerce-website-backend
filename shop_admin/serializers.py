from rest_framework import serializers
from .models import ShopAdminAccount

class ShopAdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAdminAccount
        fields = ['email', 'username', 'password', 'is_staff', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Password hashing will be handled in the model's save() method
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # If password is being updated, handle it
        if 'password' in validated_data:
            instance.password = validated_data['password']
        return super().update(instance, validated_data)

class ShopAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        if not data.get('email') and not data.get('username'):
            raise serializers.ValidationError("Either email or username must be provided.")
        if not data.get('password'):
            raise serializers.ValidationError("Password is required.")
        return data
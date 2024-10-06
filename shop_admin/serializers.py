from rest_framework import serializers
from .models import ShopAdminAccount
from django.contrib.auth.hashers import make_password

class ShopAdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAdminAccount
        fields = ['id', 'display_id', 'email', 'username', 'password', 'is_staff', 'is_admin', 'is_approved']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])

        # Only assign display_id if the account is approved
        if validated_data.get('is_approved', False):
            last_display_id = ShopAdminAccount.objects.filter(is_approved=True).order_by('display_id').last()
            if last_display_id is not None:
                validated_data['display_id'] = last_display_id.display_id + 1
            else:
                validated_data['display_id'] = 1

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])  # Hash the new password
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

        email = data.get('email')
        username = data.get('username')
        
        # Attempt to retrieve the user based on email or username
        try:
            if email:
                admin_account = ShopAdminAccount.objects.get(email=email)
            else:
                admin_account = ShopAdminAccount.objects.get(username=username)
        except ShopAdminAccount.DoesNotExist:
            raise serializers.ValidationError("Account with the provided credentials does not exist.")

        # Check if the password matches
        if not admin_account.check_password(data['password']):
            raise serializers.ValidationError("Invalid password.")
        
        # Check if the account is approved
        if not admin_account.is_approved:
            raise serializers.ValidationError("Your account is pending approval. Please wait for admin approval.")

        return data

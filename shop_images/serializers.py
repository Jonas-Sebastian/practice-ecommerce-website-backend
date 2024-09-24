from rest_framework import serializers
from .models import HeroImage

class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = ['id', 'image', 'uploaded_at']
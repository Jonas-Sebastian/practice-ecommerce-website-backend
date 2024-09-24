from rest_framework import viewsets
from .models import HeroImage
from .serializers import HeroImageSerializer

class HeroImageViewSet(viewsets.ModelViewSet):
    queryset = HeroImage.objects.all()
    serializer_class = HeroImageSerializer

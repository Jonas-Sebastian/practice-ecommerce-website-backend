from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShopAdminAccount
from .serializers import ShopAdminAccountSerializer, ShopAdminLoginSerializer

class ShopAdminAccountCreateView(generics.CreateAPIView):
    queryset = ShopAdminAccount.objects.all()
    serializer_class = ShopAdminAccountSerializer

class ShopAdminLoginView(APIView):
    def post(self, request):
        serializer = ShopAdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                if email:
                    user = ShopAdminAccount.objects.get(email=email)
                elif username:
                    user = ShopAdminAccount.objects.get(username=username)
                else:
                    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

                if user and user.check_password(password):
                    return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
            except ShopAdminAccount.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
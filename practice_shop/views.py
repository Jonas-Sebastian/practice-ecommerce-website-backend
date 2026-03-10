from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsAjaxRequest

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAjaxRequest] 
    http_method_names = ['post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request):

        query = request.data.get('q', '').strip()
        category_id = request.data.get('category', None)

        filters = Q(available=True)

        if query:
            filters &= (Q(name__icontains=query) | Q(description__icontains=query))

        if category_id:
            try:
                filters &= Q(category__id=int(category_id))
            except ValueError:
                return Response({"detail": "Invalid category ID."}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(filters)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='detail')
    def detail(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAjaxRequest]
    http_method_names = ['post', 'patch', 'head', 'options']

    def get_serializer_class(self):
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        if not request.data:
            orders = self.get_queryset()
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='detail')
    def detail(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if 'status' not in request.data:
            return Response({"detail": "Only order status can be updated."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='status-choices')
    def get_status_choices(self, request):
        status_choices = [{'value': key, 'label': label} for key, label in Order.STATUS_CHOICES]
        return Response(status_choices)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAjaxRequest]
    http_method_names = ['post', 'head', 'options']

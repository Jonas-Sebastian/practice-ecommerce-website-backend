from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '').strip()  # Sanitize query input
        category_id = request.query_params.get('category', None)

        # Start with an empty filter, only add conditions if query or category_id is provided
        filters = Q()

        if query:
            filters |= Q(name__icontains=query) | Q(description__icontains=query)

        if category_id:
            try:
                filters &= Q(category__id=int(category_id))  # Ensure category_id is a valid integer
            except ValueError:
                return Response({"detail": "Invalid category ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch products that match the filters and are available
        products = Product.objects.filter(filters, available=True)

        # Serialize the filtered products
        serializer = self.get_serializer(products, many=True)

        # Return the results (empty list if no products match the filter)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """Create a new order."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update the status of an existing order."""
        order = get_object_or_404(Order, pk=pk)
        if 'status' not in request.data:
            return Response({"detail": "Only order status can be updated."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Fetch a single order with its items and payment details."""
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='status-choices')
    def get_status_choices(self, request):
        """Return the status choices defined in the Order model."""
        status_choices = [{'value': key, 'label': label} for key, label in Order.STATUS_CHOICES]
        return Response(status_choices)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

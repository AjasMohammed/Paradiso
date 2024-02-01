from shop.models import Product, Category
from shop.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class CategoryProducts(APIView):
    """
    Retrives Products from a specific category
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        category_name = request.query_params.get('category')
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category).select_related('category')
        serializer = ProductSerializer(products, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
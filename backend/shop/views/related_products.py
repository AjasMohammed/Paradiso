from shop.models import Product
from shop.serializers import CardProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
import time


class RelatedProducts(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        product_id = request.query_params.get('productId')
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subCategory')

        products = Product.objects.select_related('category', 'subcategory').filter(
            Q(subcategory=subcategory) & Q(
                category=category) & ~Q(id=product_id)
        )
        serializer = CardProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

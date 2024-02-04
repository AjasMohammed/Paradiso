from shop.models import Product
from shop.serializers import ProductViewSerializer, CardProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Window, F
from django.db.models.functions import RowNumber
from Utility.set_cache_headers import set_cache_headers


class ProductsView(APIView):
    """
    Retrives 20 Products from each categories 
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        products = Product.objects.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('category__id')],
            )
        ).filter(row_number__lte=10)
        serializer = CardProductSerializer(products, many=True)
        data = serializer.data

        ordered_products = {}
        for item in data:
            category_name = item['category']['name']
            if category_name not in ordered_products.keys():
                ordered_products[category_name] = []
            ordered_products[category_name].append(item)

        response = set_cache_headers(Response(ordered_products, status=status.HTTP_200_OK))

        return response



class SingleProductView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ProductViewSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LikeProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.likes_count += 1
        product.save()

        return Response({'message': 'Liked Product'}, status=status.HTTP_200_OK)
from shop.models import Product, Category, SubCategory
from shop.serializers import ProductViewSerializer, SubCategorySerializer, CategoryProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from Utility.set_cache_headers import set_cache_headers

class CategoryProducts(APIView):
    """
    Retrives Products from a specific category
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        category_name = request.query_params.get('category')
        subcategory_name = request.query_params.get('subcategory')
        if subcategory_name == 'undefined':
            products = Product.objects.filter(
                category__name=category_name).select_related('category')
        else:
            products = Product.objects.filter(
                subcategory__name=subcategory_name).select_related('subcategory')
        serializer = CategoryProductSerializer(products, many=True)

        response =  set_cache_headers(Response(serializer.data, status=status.HTTP_200_OK))
        return response


class GetSubCategories(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, name):
        sub_categories = SubCategory.objects.filter(
            product__category__name=name, card_view=True).distinct()
        serializer = SubCategorySerializer(sub_categories, many=True)

        response =  set_cache_headers(Response(serializer.data, status=status.HTTP_200_OK))
        return response

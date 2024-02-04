from shop.models import Product
from shop.serializers import ProductViewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q




class SearchQuery(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get('query')
        results = Product.objects.filter(Q(name__icontains=keyword) | Q(
            category__name__icontains=keyword) | Q(subcategory__name__icontains=keyword))
        if results:
            serializer = ProductViewSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

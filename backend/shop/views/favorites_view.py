from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from shop.models import Favorite, Product
from shop.serializers import FavoriteSerializer


class ViewFavorite(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        user = request.user
        if id:
            favorite = Favorite.objects.get(
                user=request.user).products.filter(id=id)
            if favorite.exists():
                return Response(True, status=status.HTTP_200_OK)
            return Response(False, status=status.HTTP_200_OK)
        else:
            try:
                favorite = Favorite.objects.get(user=user)
                print(favorite)
                serializer = FavoriteSerializer(favorite)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Favorite.DoesNotExist:
                return Response(False)

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        favorite.products.add(product)

        return Response({'message': 'Added to Favorites Successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        try:
            favorite = Favorite.objects.get(user=request.user)
            favorite.products.remove(product)
            return Response({'message': 'Removed from Favorites Successfully'}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({'message': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)

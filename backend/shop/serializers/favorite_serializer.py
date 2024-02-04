from rest_framework import serializers
from shop.models import Favorite
from .product_serializers import ProductViewSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    products = ProductViewSerializer(many=True)

    class Meta:
        model = Favorite
        fields = "__all__"


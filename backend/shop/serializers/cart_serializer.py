from rest_framework import serializers
from shop.models import CartItem, Cart
from .product_serializers import ProductViewSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductViewSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"
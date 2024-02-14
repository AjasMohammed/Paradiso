from rest_framework import serializers
from shop.models import CartItem, Cart, Product
from .product_serializers import CheckoutSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = CheckoutSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"
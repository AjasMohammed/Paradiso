from rest_framework import serializers
from shop.models import Order, OrderItem
from .product_serializers import ProductViewSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductViewSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

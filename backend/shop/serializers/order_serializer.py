from rest_framework import serializers
from shop.models import Order, OrderItem
from .product_serializers import ProductViewSerializer
import re


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductViewSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, read_only=True, source="orderitem_set")

    class Meta:
        model = Order
        fields = "__all__"

    def validate_phone(self, phone):
        pattern = r'^(\+?\d+)(\d{10})$'
        phone = re.sub(pattern, r'\1 \2', phone) 
        return phone

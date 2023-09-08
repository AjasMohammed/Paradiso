from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    productimage_set = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Favorite
        fields = "__all__"
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

        
    # def create(self, validated_data):
    #     # Extract the category and tags PKs from the validated data
    #     category_pk = validated_data.pop('category', None)
    #     tags_pks = validated_data.pop('tags', [])

    #     # Assuming you have a method to get an existing category and tags by PK
    #     category = Category.objects.get(pk=category_pk) if category_pk else None
    #     tags = Tag.objects.filter(pk__in=tags_pks)

    #     # Create the product with the modified validated data
    #     product = Product.objects.create(category=category, **validated_data)

    #     # Add the existing tags to the product
    #     product.tags.set(tags)

    #     return product

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


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"


from rest_framework import serializers
from shop.models import Product, ProductImage
from .category_serializer import CategorySerializer
from .sub_category_serializer import SubCategorySerializer
from .variant_serializer import VarientSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()

    productimage_set = ProductImageSerializer(many=True, read_only=True)
    variants_set = VarientSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategoryProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    productimage_set = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'current_price', 'raw_price',
                  'discount', 'category', 'subcategory', 'productimage_set']


class CardProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    productimage_set = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'current_price', 'raw_price',
                  'discount', 'category', 'productimage_set']


class CheckoutSerializer(serializers.ModelSerializer):
    productimage_set = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'current_price', 'raw_price',
                  'discount', 'productimage_set']

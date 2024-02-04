from rest_framework import serializers
from shop.models import Variants


class VarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = '__all__'


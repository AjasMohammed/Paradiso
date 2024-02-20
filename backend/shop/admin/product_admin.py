from django.contrib import admin
from shop.models import ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'current_price',
                    'raw_price', 'get_subcategory_name')
    list_display_links = ('id', 'name', 'current_price', 'raw_price')
    list_filter = ('category', 'brand')
    search_fields = ('name__istartswith', 'name__icontains')
    inlines = [ProductImageInline]

    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None
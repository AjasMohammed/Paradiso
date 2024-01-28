from asyncio import format_helpers
import mimetypes
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_filter = ('category', 'brand')
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # list_display = ('product', 'image_preview')
    model = ProductImage
    readonly_fields = ('image_preview',)

    def view_image(self, obj):
        # Generate the URL to the image
        image_url = obj.image.url

        # Read the image content
        with open(image_url, 'rb') as f:
            image_data = f.read()

        # Determine the content type based on the file extension
        content_type, _ = mimetypes.guess_type(image_url)
        if not content_type:
            content_type = 'application/octet-stream'  # Fallback content type

        # Set the appropriate content type in the response
        response = HttpResponse(image_data, content_type=content_type)
        return response
    view_image.short_description = 'View Image'

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="Image" style="max-height: 100px; max-width: 100px;" />')

    image_preview.short_description = 'Image Preview'


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'is_paid', 'is_delivered', 'amount']
    list_filter = ['is_paid', 'is_delivered']
    # Specify the order of fields
    fields = ('user', 'amount', 'address', 'phone')


    inlines = [OrderItemsInline]


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_diplay = ['user']
    inlines = [CartItemInline]


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(OrderItem)
admin.site.register(Brand)
admin.site.register(Variation)
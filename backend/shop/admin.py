from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_filter = ('category', 'tags')
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'is_paid', 'is_delivered', 'amount']
    list_filter = ['is_paid', 'is_delivered']
    # Specify the order of fields
    fields = ('user', 'display_selected_products', 'amount', 'address', 'phone')

    readonly_fields = ('display_selected_products',)  # Add this line to make the field readonly

    def display_selected_products(self, obj):
        # Create a string representation of the selected products
        selected_products = '\n'.join(f"{index+1} - {str(product)}" for index, product in enumerate(obj.products.all()))
        return selected_products

    display_selected_products.short_description = 'Selected Products'  # Set the field label


    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "products":
    #         # Filter products based on the selected order
    #         order_id = request.resolver_match.kwargs.get('object_id')
    #         if order_id:
    #             order = Order.objects.get(pk=order_id)
    #             kwargs["queryset"] = order.products.all()
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)




admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Favorite)

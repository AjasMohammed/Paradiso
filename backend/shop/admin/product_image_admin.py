import mimetypes
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

class ProductImageAdmin(admin.ModelAdmin):
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
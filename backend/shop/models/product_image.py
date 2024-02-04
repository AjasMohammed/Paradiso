from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from Utility.compress_image import compress_image



class ProductImage(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)

    def get_image_upload_path(self, filename):
        directory_name = f'{self.product.id}'
        path = f'products/{directory_name}/{filename}'
        return path

    image = models.ImageField(upload_to=get_image_upload_path, max_length=5000)
    thumbnail = models.ImageField(
        upload_to='products/thumbnails', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        if not self.thumbnail:
            img = Image.open(self.image)
            output_size = (200, 200)
            img.thumbnail(output_size)

            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_io.seek(0)

            self.thumbnail.save(self.image.name, File(thumb_io), save=False)
            super().save(*args, **kwargs)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        db_table = "product_image"

    def __str__(self):
        return f"Image of {self.product.name}"

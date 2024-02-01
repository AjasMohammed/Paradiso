from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File


class Variants(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    color = models.CharField(verbose_name="Varient Colors", max_length=50)

    def get_image_upload_path(self, filename):
        directory_name = f'{self.product.id}'
        path = f'products/{directory_name}/varients/{filename}'
        return path

    image = models.ImageField(upload_to=get_image_upload_path, max_length=500)
    thumbnail = models.ImageField(
        upload_to='products/thumbnails', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
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
        verbose_name = 'Variant'
        verbose_name_plural = 'Variants'
        db_table = "variant"

    def __str__(self):
        return f"Image of {self.product.name}"

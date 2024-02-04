from collections.abc import Iterable
from django.db import models
from Utility.compress_image import compress_image


class SubCategory(models.Model):

    def get_image_upload_path(self, filename):
        directory_name = f'{self.name}'
        path = f'subcategory/{directory_name}/{filename}'
        return path

    name = models.CharField(unique=True, max_length=255)
    card_view = models.BooleanField(default=False)
    image_primary = models.ImageField(
        upload_to=get_image_upload_path, max_length=5000, null=True, blank=True)
    image_secondary = models.ImageField(
        upload_to=get_image_upload_path, max_length=5000, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.image_primary:
            self.image_primary = compress_image(self.image_primary)

        if self.image_secondary:
            self.image_secondary = compress_image(self.image_secondary)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        db_table = "sub_category"

    def __str__(self) -> str:
        return self.name

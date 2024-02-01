from django.db import models


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(verbose_name="Brand URL",
                          max_length=200, null=True, blank=True)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = "brand"

    def __str__(self) -> str:
        return self.name

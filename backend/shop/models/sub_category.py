from django.db import models


class SubCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        db_table = "sub_category"

    def __str__(self) -> str:
        return self.name

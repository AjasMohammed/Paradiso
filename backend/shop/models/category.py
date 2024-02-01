from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = "category"

    def __str__(self):
        return self.name


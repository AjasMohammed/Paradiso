from django.db import models


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    raw_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('shop.SubCategory', verbose_name="Sub Category", on_delete=models.CASCADE)
    brand = models.ForeignKey(
        'shop.Brand', on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(max_length=100000, null=True, blank=True)

    likes_count = models.IntegerField()
    is_new = models.BooleanField()

    class Meta:
        ordering = ['id']
        app_label = 'shop'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = "product"

    def __str__(self):
        return self.name
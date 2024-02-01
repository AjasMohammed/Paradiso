from django.db import models
from shop.models import Order, Product


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        db_table = "order_item"

    def __str__(self):
        return f"{self.pk}-{self.order.pk}"

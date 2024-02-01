from django.db import models
from authentication.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(max_length=10000)
    city = models.CharField(max_length=1000)
    phone = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=8)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = "order"

    def __str__(self):
        return f"{self.user}-{self.pk}"

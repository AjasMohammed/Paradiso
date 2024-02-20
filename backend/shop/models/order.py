from django.db import models
from authentication.models import CustomUser


class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(max_length=10000)
    city = models.CharField(max_length=1000)
    phone = models.CharField(max_length=14)
    zipcode = models.CharField(max_length=8)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='pending')

    class Meta:
        app_label = 'shop'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = "order"

    def __str__(self):
        return f"{self.user}-{self.pk}"

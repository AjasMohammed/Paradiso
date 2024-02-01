from django.db import models
from authentication.models import CustomUser



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        total = self.cartitem_set.aggregate(total=models.Sum(
            models.F('product__price') * models.F('quantity')))['total']
        self.total = total if total is not None else 0
        self.save()
        return self.total

    class Meta:
        app_label = 'shop'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = "cart"

    def __str__(self):
        return f'Cart for {self.user.username}'

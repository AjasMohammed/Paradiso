from django.db import models
from authentication.models import CustomUser
from shop.models import Product


class Favorite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    class Meta:
        app_label = 'shop'
        verbose_name = 'Favotite'
        verbose_name_plural = 'Favotites'
        db_table = "favorite"

    def __str__(self):
        return f"{self.user.email}'s Favorite"

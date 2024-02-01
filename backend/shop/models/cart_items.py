from django.db import models
from shop.models import Product, Cart


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the total price of the cart whenever a CartItem is saved
        self.cart.update_total()

    class Meta:
        app_label = 'shop'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        db_table = "cart_item"

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

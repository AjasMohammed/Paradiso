from django.db import models
from authentication.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    description = models.TextField(max_length=100000, null=True, blank=True)

    # rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def dirName(self, filename):
        directory_name = f'{self.product.name}_{self.product.id}'
        path = f'products/{directory_name}/{filename}'
        return path

    image = models.ImageField(upload_to=dirName, max_length=500)



    def __str__(self):
        return f"Image of {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        total = self.cartitem_set.aggregate(total=models.Sum(models.F('product__price') * models.F('quantity')))['total']
        self.total = total if total is not None else 0
        self.save()

    def __str__(self):
        return f'Cart for {self.user.username}'
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the total price of the cart whenever a CartItem is saved
        self.cart.update_total()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Favorite"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # products = models.ManyToManyField(Product, through='OrderItem')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(max_length=10000)
    city = models.CharField(max_length=1000)
    phone = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=8)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}-{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}-{self.order.pk}"
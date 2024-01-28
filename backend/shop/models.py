from django.db import models
from authentication.models import CustomUser
from PIL import Image
from io import BytesIO
from django.core.files import File


class SubCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)
    class Meta:
        app_label = 'shop'
    
    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subcategory = models.ManyToManyField(SubCategory, verbose_name="Sub Category")
    class Meta:
        app_label = 'shop'
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=255)
    url = models.URLField(verbose_name="Brand URL",
                          max_length=200, null=True, blank=True)

    class Meta:
        app_label = 'shop'
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(max_length=100000, null=True, blank=True)

    class Meta:
        ordering = ['id']
        app_label = 'shop'
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def get_image_upload_path(self, filename):
        directory_name = f'{self.product.id}'
        path = f'products/{directory_name}/{filename}'
        return path

    image = models.ImageField(upload_to=get_image_upload_path, max_length=500)
    thumbnail = models.ImageField(
        upload_to='products/thumbnails', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            img = Image.open(self.image)
            output_size = (200, 200)
            img.thumbnail(output_size)

            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_io.seek(0)

            self.thumbnail.save(self.image.name, File(thumb_io), save=False)
            super().save(*args, **kwargs)

    class Meta:
        app_label = 'shop'
    
    def __str__(self):
        return f"Image of {self.product.name}"


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(verbose_name="Varient Colors", max_length=50)

    def get_image_upload_path(self, filename):
        directory_name = f'{self.product.id}'
        path = f'products/{directory_name}/varients/{filename}'
        return path

    image = models.ImageField(upload_to=get_image_upload_path, max_length=500)
    thumbnail = models.ImageField(
        upload_to='products/thumbnails', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            img = Image.open(self.image)
            output_size = (200, 200)
            img.thumbnail(output_size)
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_io.seek(0)
            self.thumbnail.save(self.image.name, File(thumb_io), save=False)
            super().save(*args, **kwargs)

    class Meta:
        app_label = 'shop'
    
    def __str__(self):
        return f"Image of {self.product.name}"


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

    class Meta:
        app_label = 'shop'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"


class Favorite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    class Meta:
        app_label = 'shop'
    
    def __str__(self):
        return f"{self.user.username}'s Favorite"


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
    
    def __str__(self):
        return f"{self.user}-{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        app_label = 'shop'
    
    def __str__(self):
        return f"{self.pk}-{self.order.pk}"

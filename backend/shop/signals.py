from shop.models import Product, ProductImage, Variants, Order, Cart
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
import os


@receiver(post_save, sender=Order)
def clear_cart(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        cart = Cart.objects.get(user=user)
        cart.delete()


@receiver(pre_delete, sender=Product)
def cleanup_db(sender, instance, **kwargs):
    product_image = ProductImage(product=instance)
    image_path = product_image.image.path
    thumbnail_path = product_image.thumbnail.path
    delete_img(image_path)
    delete_img(thumbnail_path)

    variants = Variants.objects.filter(product=instance)
    for variant in variants:
        delete_img(variant.image.path)
        delete_img(variant.thumbnail.path)


def delete_img(path):
    if os.path.exists(path):
        os.remove(path)

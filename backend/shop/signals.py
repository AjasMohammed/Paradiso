from shop.models import Product, ProductImage, Variants, Order, Cart, SubCategory
from django.db.models.signals import pre_delete, post_save, pre_save
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


@receiver(post_save, sender=SubCategory)
def cleanup_subcategory(sender, instance, **kwargs):
    if instance.image_primary:
        directory_path = os.path.dirname(instance.image_primary.path)
        # List all files in the directory
        directory_files = os.listdir(directory_path)
        # Get the filenames of the images associated with the SubCategory instance
        used_filenames = set()
        if instance.image_primary:
            used_filenames.add(os.path.basename(instance.image_primary.path))
        if instance.image_secondary:
            used_filenames.add(os.path.basename(instance.image_secondary.path))

        # Delete unused images from the directory
        for filename in directory_files:
            if filename not in used_filenames:
                file_path = os.path.join(directory_path, filename)
                delete_img(file_path)


def delete_img(path):
    if os.path.exists(path):
        os.remove(path)

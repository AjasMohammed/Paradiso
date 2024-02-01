from django.core.management.base import BaseCommand
from shop.models import *
from django.db.models import Count, F, Value
from django.db.models.functions import Coalesce


class Command(BaseCommand):
    help = 'Dump garbage data from database'

    def handle(self, *args, **kwargs):

        products = Product.objects.annotate(
            num_images=Count('productimage')).filter(num_images=0)
        if products:
            for product in products:
                product.delete()

        products = Product.objects.filter(productimage__isnull=True)
        if products:
            for product in products:
                product.delete()

        self.stdout.write(self.style.SUCCESS(
            '\nData Dumped successfully.\n'))

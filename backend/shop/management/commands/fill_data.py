import csv
from django.core.management.base import BaseCommand
from shop.models import *
import requests
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Import data from CSV file to database'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.example.com'
    }

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            index = 0
            for data in reader:
                category = data.get('category', None)
                subcategory = data.get('subcategory', None)
                name = data.get('name', None)
                price = data.get('price', None)
                brand = data.get('brand', None)
                brand_url = data.get('brand_url', None)
                variation_0_color = data.get('variation_0_color', None)
                variation_1_color = data.get('variation_1_color', None)
                variation_0_image = data.get('variation_0_image', None)
                variation_1_image = data.get('variation_1_image', None)
                image_url = data.get('image_url', None)
                description = data.get('description', None)

                index += 1
                if subcategory:
                    subcategory_mod, _ = SubCategory.objects.get_or_create(
                        name=subcategory)
                if category:
                    category_mod, _ = Category.objects.get_or_create(
                        name=category)
                    category_mod.subcategory.add(subcategory_mod)
                if brand:
                    brand_mod, _ = Brand.objects.get_or_create(
                        name=brand, url=brand_url)
                else:
                    brand_mod = None

                status = self.check_status(image_url)
                if not status:
                    self.stdout.write(self.style.NOTICE(f'Index - {index}'))
                    continue
                product = Product(
                    name=name,
                    price=round(float(price), 2),
                    category=category_mod,
                    brand=brand_mod,
                    description=description
                )
                product.save()

                product_image = ProductImage(product=product)
                self.save_image(name=name, image_url=image_url,
                                instance=product_image)

                varient_0 = Variation(product=product, color=variation_0_color)
                self.save_image(name=name, image_url=variation_0_image,
                                instance=varient_0, color=variation_0_color)

                varient_1 = Variation(product=product, color=variation_1_color)
                self.save_image(name=name, image_url=variation_1_image,
                                instance=varient_1, color=variation_1_color)

                self.stdout.write(self.style.SUCCESS(f'Index - {index}'))

        self.stdout.write(self.style.SUCCESS(
            '\nData imported successfully.\n'))

    def check_status(self, url):
        if url:
            response = requests.get(url, headers=self.headers)
            return response.status_code != 404
        return False

    def save_image(self, name, image_url, instance, color=None):
        image_status = self.check_status(image_url)
        if image_url:
            img_response = requests.get(image_url, headers=self.headers)
            if img_response.status_code == 200:
                img_content = img_response.content
                if color:
                    name += f" {color}_varient"
                img_name = name.lower().replace(' ', '_') + '.jpg'
                instance.image.save(img_name, ContentFile(img_content), save=True)
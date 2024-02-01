import csv
from django.core.management.base import BaseCommand
from shop.models import *
import requests
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


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

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            index = 0
            for data in reader:
                category = data.get('category', None)
                subcategory = data.get('subcategory', None)
                name = data.get('name', None)
                current_price = data.get('current_price', None)
                raw_price = data.get('raw_price', None)
                discount = data.get('discount', None)
                likes_count = data.get('likes_count', 0)
                is_new = data.get('is_new', False)
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
                    discount=discount,
                    likes_count=likes_count,
                    is_new=is_new,
                    current_price=round(float(current_price), 2),
                    raw_price=round(float(raw_price), 2),
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
            try:
                response = requests.get(url, headers=self.headers)
                return response.status_code != 404
            except:
                return False
        return False

    def save_image(self, name, image_url, instance, color=None):
        image_status = self.check_status(image_url)
        if image_status:
            img_response = requests.get(image_url, headers=self.headers)
            if img_response.status_code == 200:
                img_content = img_response.content
                if color:
                    name += f" {color}_varient"
                img_name = name.lower().replace(' ', '_') + '.jpg'
                try:
                    instance.image.save(img_name, ContentFile(img_content), save=True)
                except :
                    img = Image.open(BytesIO(img_content))
                    img = img.convert("RGB")
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    instance.image.save(img_name, ContentFile(img_byte_arr.getvalue()), save=True)
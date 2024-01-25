import csv
from django.core.management.base import BaseCommand
from shop.models import * 

class Command(BaseCommand):
    help = 'Import data from CSV file to database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if it exists

            for row in reader:
                Product.objects.create(column1=row[0], column2=row[1]) 

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))

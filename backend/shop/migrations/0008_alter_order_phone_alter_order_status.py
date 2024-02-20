# Generated by Django 5.0.1 on 2024-02-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ('returned', 'Returned')], default='pending', max_length=100),
        ),
    ]

# Generated by Django 4.2.13 on 2024-06-07 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_address_order_city_order_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='user',
        ),
    ]

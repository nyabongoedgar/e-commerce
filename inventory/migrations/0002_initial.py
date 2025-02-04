# Generated by Django 4.2.13 on 2024-05-16 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_product', to='products.product'),
        ),
    ]

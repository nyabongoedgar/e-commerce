# Generated by Django 4.2.13 on 2024-05-16 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wishlist', '0001_initial'),
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='wishlist_items',
            field=models.ManyToManyField(related_name='users', to='wishlist.wishlistitem'),
        ),
    ]

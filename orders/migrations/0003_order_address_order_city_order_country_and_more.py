# Generated by Django 4.2.13 on 2024-06-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='PENDING', max_length=20),
        ),
    ]

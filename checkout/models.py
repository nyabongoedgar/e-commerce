from django.db import models
from accounts.models import CustomUser  # Importing User model from auth app

class Payment(models.Model):
    MOBILE_MONEY = 'MM'
    CARD = 'CARD'
    PAYMENT_METHOD_CHOICES = [
        (MOBILE_MONEY, 'Mobile Money'),
        (CARD, 'Card'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.method} - {self.transaction_id}'

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} - {self.address}'


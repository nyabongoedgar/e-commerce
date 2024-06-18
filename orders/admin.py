from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_status', 'is_in_cart', 'created_at', 'updated_at')
    search_fields = ('user__username', 'address', 'postal_code', 'city', 'country')

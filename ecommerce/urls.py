"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urls import urlpatterns as drf_url_patterns

# Combine all URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    # Add Django Rest Framework authentication URLs
    path('api-auth/', include((drf_url_patterns, 'rest_framework'), namespace='rest_framework')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/wishlist', include('wishlist.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/orders', include('orders.urls')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/checkout/', include('checkout.urls')),
    
]


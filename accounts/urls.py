from django.urls import path
from .views import register, user_login, send_password_reset_email, reset_password

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('send-password-reset-email', send_password_reset_email, name="send_password_reset_email"),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
]

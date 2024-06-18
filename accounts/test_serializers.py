# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse_lazy
from .models import CustomUser
from .serializers import UserSerializer

class UserSerializerTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_user_serializer(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_user(self):
        url = reverse_lazy('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_invalid_user_serializer(self):
        # Missing required field 'password'
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_unique_username_validation(self):
        # Create a user to conflict with
        CustomUser.objects.create_user(username='existinguser', email='existing@example.com', password='testpassword')

        # Attempt to create a user with the same username
        data = {
            'username': 'existinguser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_unique_email_validation(self):
        # Create a user to conflict with
        CustomUser.objects.create_user(username='testuser', email='existing@example.com', password='testpassword')

        # Attempt to create a user with the same email
        data = {
            'username': 'newuser', 
            'email': 'existing@example.com',
            'password': 'testpassword'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

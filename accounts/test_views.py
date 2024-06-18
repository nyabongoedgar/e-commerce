from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail

UserModel = get_user_model()

class TestUserViews(APITestCase):
    def setUp(self):
        self.user_data = {'username': 'test_user', 'email': 'test@example.com', 'password': 'test_password'}
        self.user = UserModel.objects.create_user(**self.user_data)

    def test_register_view(self):
        url = reverse_lazy('register')
        data = {'username': 'test_user2', 'email': 'test2@example.com', 'password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserModel.objects.filter(username='test_user2').exists())

        # Negative tests
        # Duplicate username
        secondUser = {'username': 'test_user2', 'password': 'test_password'}
        response2 = self.client.post(url, secondUser, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

        # Missing fields
        thirdUser = {'email': 'test2@example.com'}
        response3 = self.client.post(url, thirdUser, format='json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_view(self):
        url = reverse_lazy('login')
        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # Negative tests
        # Incorrect password
        data = {'username': 'test_user', 'password': 'wrong_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

        # Nonexistent username
        data = {'username': 'nonexistent_user', 'password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_send_password_reset_email_view(self):
        url = reverse_lazy('send_password_reset_email')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json', **{'HTTP_HOST': 'testserver'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)


        # Negative tests
        # Nonexistent email
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(url, data, format='json', **{'HTTP_HOST': 'testserver'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Missing email field
        data = {}
        response = self.client.post(url, data, format='json', **{'HTTP_HOST': 'testserver'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_reset_password_view(self):
        # Generate password reset token
        token_generator = default_token_generator
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)

        url = reverse_lazy('reset_password', kwargs={'uidb64': uidb64, 'token': token})
        data = {'new_password': 'new_test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

         # Negative tests
        # Invalid token
        invalid_token = 'invalid-token'
        url = reverse_lazy('reset_password', kwargs={'uidb64': uidb64, 'token': invalid_token})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Invalid uidb64
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(9999))
        url = reverse_lazy('reset_password', kwargs={'uidb64': invalid_uidb64, 'token': token})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Missing new_password field
        url = reverse_lazy('reset_password', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Invalid reset link', response.data['error'])

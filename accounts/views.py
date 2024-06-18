from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_password_reset_email(request):
    email = request.data.get('email')
    domain = request.META['HTTP_HOST']
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return Response({'error': 'No user found with this email'}, status=400)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f'{domain}/{uid}/{token}/'  # Replace example.com with your domain
    send_mail(
        'Password Reset',
        f'Click the link to reset your password: {reset_link}',
        'from@example.com',  # Replace with your email
        [email],
        fail_silently=False,
    )
    return Response({'message': 'Password reset email sent'})

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully'})
    return Response({'error': 'Invalid reset link'}, status=400)

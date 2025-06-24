from accounts.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import UserSerializer, ChangePasswordSerializer, RegisterSerializer, PasswordResetSerializer
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] 

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not check_password(serializer.validated_data['old_password'], user.password):
                return Response({'old_password': 'Hibás régi jelszó!'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Jelszó sikeresen megváltoztatva.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                reset_link = f"http://localhost:8000/reset-password/{user.pk}/{token}/"
                send_mail(
                    'Jelszó visszaállítás',
                    f'Kattints ide a jelszó visszaállításához: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'detail': 'Jelszó visszaállítási email elküldve.'})
            except User.DoesNotExist:
                return Response({'detail': 'Nincs ilyen email.'}, status=404)
        return Response(serializer.errors, status=400)
    
class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Sikeres regisztráció!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProviderListView(APIView):
    def get(self, request):
        providers = User.objects.filter(role='provider')
        serializer = UserSerializer(providers, many=True)
        return Response(serializer.data)
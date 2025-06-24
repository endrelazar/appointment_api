from .api_views import UserViewSet, ProfileView, ChangePasswordView, RegisterView, ProviderListView, ProfileUpdateView, PasswordResetView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='api-profile'),
    path('register/', RegisterView.as_view(), name='api-register'),
    path('', include(router.urls)),
    path('change-password/', ChangePasswordView.as_view(), name='api-change-password'),
    path('providers/', ProviderListView.as_view(), name='api-provider-list'),
    path('profile/update/', ProfileUpdateView.as_view(), name='api-profile-update'),
    path('password-reset/', PasswordResetView.as_view(), name='api-password-reset'),
]
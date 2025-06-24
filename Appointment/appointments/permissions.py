from rest_framework.permissions import BasePermission

class IsProvider(BasePermission):
    """
    Csak provider szerepű felhasználónak engedélyezett.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'provider'
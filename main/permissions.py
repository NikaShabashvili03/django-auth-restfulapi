from rest_framework.permissions import BasePermission
from main.models import Member
from rest_framework.exceptions import PermissionDenied

class IsAuthenticatedCustom(BasePermission):
    """
    Custom permission to allow only authenticated users who are instances of Member.
    """

    def has_permission(self, request, view):
        if request.user and isinstance(request.user, Member):
            if not request.user.is_active:
                raise PermissionDenied(f"User not active. come tomorrow on 07:33")
            return True
        return False

class AllowAny(BasePermission):
    """
    Allow access to any request, regardless of authentication or authorization.
    """
    
    def has_permission(self, request, view):
        return True
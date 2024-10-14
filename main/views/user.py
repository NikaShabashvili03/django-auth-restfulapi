# views.py
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import LoginSerializer, ProfileSerializer
from ..models.user import Member
from ..permissions import IsAuthenticatedCustom, AllowAny
from ..authentication import generate_jwt
from django.utils import timezone

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        print(user)
        
        # Generate JWT for the user
        token = generate_jwt(user.email)

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return Response({
            'token': token,
        }, status=status.HTTP_200_OK)
        
class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedCustom]  # Use the custom permission
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
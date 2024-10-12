# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import RegisterSerializer, LoginSerializer, ProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object() 
        print("User Email:", user.email) 

        serializer = self.get_serializer(user)
        return Response(serializer.data)

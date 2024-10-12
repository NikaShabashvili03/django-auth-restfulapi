# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate  # Ensure this is imported

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        # Authenticate the user
        user = authenticate(email=email, password=password)  # This line needs to be correct

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']

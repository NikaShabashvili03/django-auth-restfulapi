# serializers.py

from rest_framework import serializers
from ..models.user import Member

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = Member.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError(f"Your account is not active. Please come from {user.deadline_from} to {user.deadline_to}")
            if not user.check_password(password):
                raise serializers.ValidationError(("Invalid credentials"))
        except Member.DoesNotExist:
            raise serializers.ValidationError(("Invalid credentials"))

        attrs['user'] = user
        return attrs
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member  # Change to your custom user model
        fields = '__all__'
        
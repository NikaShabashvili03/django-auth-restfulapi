import os
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from main.models import Member
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self):
        # Load the custom JWT secret from environment variables
        self.jwt_secret = os.getenv('CUSTOM_JWT_SECRET', 'your_custom_secret_here')

    def authenticate(self, request):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer' not in auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])

            # Fetch the user from the decoded token (assuming the token contains 'email')
            email = decoded_token.get('email')
            if not email:
                raise AuthenticationFailed("Invalid token, 'email' field missing.")

            user = Member.objects.get(email=email)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.DecodeError:
            raise AuthenticationFailed("Token is invalid.")
        except Member.DoesNotExist:
            raise AuthenticationFailed("User not found.")

    def get_user(self, validated_token):
        # In case you need to override this method, you can customize user lookup here.
        user_id = validated_token.get('user_id')
        try:
            return Member.objects.get(id=user_id)
        except Member.DoesNotExist:
            raise Inva


def generate_jwt(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=5),  # Token expiration time
        'iat': datetime.utcnow(),  # Issued at time
    }
    token = jwt.encode(payload, settings.CUSTOM_JWT_SECRET, algorithm='HS256')
    return token


def decode_jwt(token):
    """
    Decodes a JWT and returns the payload if valid.
    Raises an AuthenticationFailed exception if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.CUSTOM_JWT_SECRET, algorithms=["HS256"])
        
        # Check if the token is expired
        if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
            raise AuthenticationFailed("Token has expired.")

        return payload

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token.")
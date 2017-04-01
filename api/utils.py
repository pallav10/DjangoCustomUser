from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from serializers import UserSerializer, UserProfileSerializer
import exceptions_utils
from rest_framework import status


def generate_token(user):
    # Token table is of Django Rest Framework
    # Creates the token at registration time
    token = Token.objects.create(user=user)
    # Return only the key with is associated with the object
    return token.key


def hash_password(password):
    return make_password(password)


def create_user(data):
    user_serializer = UserSerializer(data=data)
    # print(repr(user_serializer))
    if user_serializer.is_valid():
        user = user_serializer.save()
        token = Token.objects.create(user=user)
        keys = ['id', 'first_name', 'last_name', 'email', 'contact_no', 'created'
                ]  # data that we want to return as JSON response
        user_response = {k: v for k, v in user_serializer.data.iteritems() if k in keys}
        user_response['token'] = token.key
        return user_response
    else:
        raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


def update_user(data, user):
    user_serializer = UserProfileSerializer(data=data, instance=user)
    if user_serializer.is_valid():
        user_serializer.save()
        return user_serializer.data
    else:
        raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)

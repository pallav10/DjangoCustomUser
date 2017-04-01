from rest_framework import serializers
from models import User


# used for registration, it hold the value of user table with all fields.


class UserSerializer(serializers.ModelSerializer):
    # token = serializers.Field(source='my_token')

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'country_code', 'contact_no',
                  'created', 'modified', 'city', 'state', 'country')


# serialize data of user for common need of user table.
class UserProfileSerializer(serializers.ModelSerializer):
    contact_no = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'first_name', 'last_name', 'created', 'country_code', 'contact_no', 'city',
            'state', 'country', 'is_password_changed')

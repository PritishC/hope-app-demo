from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

AppUser = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = AppUser
        fields = ('url', 'email', 'password',
                  'first_name', 'last_name',
                  'college', 'mobile',
                  'subscribed')

    def create(self, validated_data):
        return AppUser.objects.create_user(**validated_data)


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user sent valid email
            try:
                validate_email(email)
            except ValidationError:
                raise

            user_request = get_object_or_404(
                AppUser,
                email=email,
            )

            email = user_request.email
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise ValidationError(msg)
        else:
            msg = _('Must include "email" and "password"')
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs

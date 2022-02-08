from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email is None:
            raise serializers.\
                ValidationError('An email address is required to log in.')
        if password is None:
            raise serializers.\
                ValidationError('A password is required to log in.')
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.\
                ValidationError('A user with this email and password was not found.')

        attrs['token'] = RefreshToken.for_user(user).access_token
        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8,
                                     write_only=True)

    class Meta:
        model = User
        # fields = ('email', 'username', 'password', )
        fields = ('id', 'username', 'email', 'password', 'cash',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

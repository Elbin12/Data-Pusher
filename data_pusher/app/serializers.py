from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Account


class SignupSerializer(ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmPassword']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already registered.")
        return value

    def validate(self, data):
        print(data, 'data')
        if data.get('password') != data.get('confirmPassword'):
            raise ValidationError('Both passwords should be same')
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

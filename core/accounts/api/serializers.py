from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()
class UserRegistrationSerilaizer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        password, password2= validated_data['password'], validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':"Passwords doesn't match"})
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        return validated_data
    

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return User.objects.create_user(**validated_data)
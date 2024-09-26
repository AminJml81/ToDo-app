from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError

from .utils import validate_user


User = get_user_model()
class UserRegistrationSerilaizer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, style={"input_type": "password"},)
    password2 = serializers.CharField(required=True, style={"input_type": "password"},)


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
    

class UserTokenLoginSerializer(serializers.Serializer):
    username_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)
    token = serializers.CharField(read_only=True)


    def validate(self, attrs):
        validated_data = super().validate(attrs)
        username_email , password= validated_data['username_email'], validated_data['password']
        request = self.context.get('request')
        user = validate_user(request, username_email, password)        
        validated_data['user']=user

        return validated_data
    

class JWTTokenObtainPairSerializer(serializers.Serializer):
    username_email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, style={"input_type": "password"}, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        username_email , password= validated_data['username_email'], validated_data['password']
        request = self.context.get('request')
        user = validate_user(request, username_email, password)     

        validated_data['access'], validated_data['refresh'] = self.create_jwt_tokens(user)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        validated_data["email"] = user.email

        return validated_data
    
    
    def create_jwt_tokens(self, user):
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access= str(token.access_token)
        return access, refresh
    

class UserActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        user_email = validated_data.get('email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise ValidationError(
                {'email':'user does not exists !!!'}
            )
        if user.is_verified:
            raise ValidationError({'email':'your account has already been activated !!!'})
        validated_data['user'] = user

        return validated_data
    

class ChangePasswordSeriliazer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    new_password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        # it checks 
        # new passwords match 
        # new password is strong 
        # the current password is correct
        validated_data =  super().validate(attrs)
        new_password , new_password2 = validated_data.get('new_password'), validated_data.get('new_password2')
        if new_password != new_password2:
            raise ValidationError({'new passwords': "new passwords doesn't match"})
        
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({'new password': list(e.messages)})


        current_password = validated_data.get('current_password')
        user = self.context.get('user')
        if not user.check_password(current_password):
            raise ValidationError({'current password': 'Wrong Password !!!'})
        return validated_data
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    new_password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)


    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        new_password , new_password2 = validated_data.get('new_password'), validated_data.get('new_password2')
        if new_password != new_password2:
            raise ValidationError({'new passwords': "new passwords doesn't match"})
        
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({'new password': list(e.messages)})
        return validated_data
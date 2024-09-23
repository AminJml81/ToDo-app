from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
#from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.backends import EmailUsernameBackend


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
    password = serializers.CharField(required=True, style={"input_type": "password"})
    token = serializers.CharField(read_only=True)


    def validate(self, attrs):
        validated_data = super().validate(attrs)
        username_email , password= validated_data['username_email'], validated_data['password']
        user = EmailUsernameBackend.authenticate(request=self.context.get('request'),username=username_email, password=password)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError({'credentials error':msg}, code='authentication')
        if not user.is_verified:
            msg = _("User is not verified.")
            raise serializers.ValidationError({'not verified': msg}, code='verification')
        
        validated_data['user']=user

        return validated_data
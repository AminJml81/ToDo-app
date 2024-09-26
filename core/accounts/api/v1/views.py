from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ..serializers import(
    UserRegistrationSerilaizer,
    UserTokenLoginSerializer,
    JWTTokenObtainPairSerializer,
    UserActivationResendSerializer,
    ChangePasswordSeriliazer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer
)
from ..utils import(
    send_email, 
    create_token_with_user,
    decode_token,
    create_token_with_email, 
    decode_token_with_email
)

User = get_user_model()


class RegistrationGenericView(GenericAPIView):
    serializer_class = UserRegistrationSerilaizer
    permission_classes = []


    def post(self, request, *args, **kwargs):
        recieved_data = request.data
        serializer = UserRegistrationSerilaizer(data=recieved_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_email = serializer.validated_data['email']
        user = get_object_or_404(User, email=user_email)
        token = create_token_with_user(user)
        send_email('email/user_activation.tpl', user_email, token)
        return Response({'detail':f'an activation email has been sent to {user_email}'}, status=status.HTTP_201_CREATED)


class TokenLoginGenericView(GenericAPIView):
    serializer_class = UserTokenLoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        recieved_data = request.data
        serializer = self.serializer_class(data = recieved_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})


class TokenLogoutGenericView(APIView):

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class JWTTokenObtainPairView(GenericAPIView):
    serializer_class = JWTTokenObtainPairSerializer
    permission_classes = []
    

    def post(self, request, *args, **kwargs):
        recieved_data = request.data
        serializer = self.get_serializer(data=recieved_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserActivationConfirmAPIView(APIView):
    permission_classes = []

    def get(self, request, token, *args, **kwargs):
        user_id = decode_token(token)
        if not user_id:
            return Response({'Message':'Token is Expired or Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, pk=user_id)
        if not user.is_verified:
            user.is_verified = True
            user.save()
            return Response({'message':'your account has been activated.'})
        else:
            return Response({'message':'your account has already been activated !!!'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserAtivationResendGenericView(GenericAPIView):
    permission_classes = []
    serializer_class = UserActivationResendSerializer

    def post(self, request, *args, **kwargs):
        recieved_data = request.data
        serilizer = self.serializer_class(data=recieved_data)
        serilizer.is_valid(raise_exception=True)
        user, user_email = serilizer.validated_data['user'], serilizer.validated_data['email']
        token = create_token_with_user(user)
        send_email('email/user_activation.tpl', user_email, token)
        return Response({'detail':f'an activation email has been sent to {user_email} Again'})
    

class ChangePasswordGenericView(GenericAPIView):
    serializer_class = ChangePasswordSeriliazer


    def post(self, request, *args, **kwargs):
        recieved_data = request.data
        user = request.user
        serializer = self.serializer_class(data = recieved_data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response('message: your password was successfully changed.')
    

class ResetPasswordGenericView(GenericAPIView):
    permission_classes = []
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        received_data = request.data
        serializer = self.serializer_class(data=received_data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data.get('email')
        token = create_token_with_email(user_email)
        send_email('email/userpassword_reset.tpl', user_email, token)
        return Response(f'we have sent an email to {user_email}.')
    

class ResetPasswordConfirmGenericView(GenericAPIView):
    permission_classes = []
    serializer_class = ResetPasswordConfirmSerializer
    
        
    def put(self, request, token, *args, **kwargs):
        user_email = decode_token_with_email(token)
        user = get_object_or_404(User, email=user_email)
        recieved_data = request.data
        serializer = self.serializer_class(data=recieved_data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'message':'your password was successfully reset'})
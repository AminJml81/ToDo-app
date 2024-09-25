from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from mail_templated import EmailMessage

from ..serializers import(
    UserRegistrationSerilaizer,
    UserTokenLoginSerializer,
    JWTTokenObtainPairSerializer,
    UserActivationResendSerializer
)
from ..utils import EmailThread, create_token, decode_token

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
        token = create_token(user)
        self.send_actvation_email(user_email, token)
        return Response({'detail':f'an activation email has been sent to {user_email}'}, status=status.HTTP_201_CREATED)
    
    def send_actvation_email(self, receiver_email, token):
        context = {'token':token, 'user_email':receiver_email}
        email = EmailThread('email/user_activation.tpl', receiver_email=[receiver_email], context=context)
        email.start()

    
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
    

class UserActivationConfirmApiView(APIView):
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
            return Response({'message':'your account has already been activated !!!'})
        

class UserAtivationResendGenericView(GenericAPIView):
    permission_classes = []
    serializer_class = UserActivationResendSerializer

    def post(self, request, *args, **kwargs):
        recieved_data = request.data
        serilizer = self.serializer_class(data=recieved_data)
        serilizer.is_valid(raise_exception=True)
        user, user_email = serilizer.validated_data['user'], serilizer.validated_data['email']
        token = create_token(user)
        self.send_actvation_email(user_email, token)
        return Response({'detail':f'an activation email has been sent to {user_email} Again'})
    
    def send_actvation_email(self, receiver_email, token):
        context = {'token':token, 'user_email':receiver_email}
        email = EmailThread('email/user_activation.tpl', receiver_email=[receiver_email], context=context)
        email.start()
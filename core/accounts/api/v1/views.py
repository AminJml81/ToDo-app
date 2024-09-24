from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from ..serializers import(
    UserRegistrationSerilaizer,
    UserTokenLoginSerializer,
    JWTTokenObtainPairSerializer
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
        email = serializer.validated_data['email']
        # TODO : send email
        return Response({'detail':f'email has been sent to {email}'}, status=status.HTTP_201_CREATED)
    

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
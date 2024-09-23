from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from ..serializers import UserRegistrationSerilaizer


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
        return Response({'detail':'email has been sent to {email}'}, status=status.HTTP_201_CREATED)
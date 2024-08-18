from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailUsernameBackend(ModelBackend):
            
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            # username can contain @ so we should check both username, email fields with given data(username) and then match it with password.
            # if thats ok, login, else Error
            user = user_model.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            
        except user_model.DoesNotExist:
            return None

    # def get_user(self, user_id, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     print('get user model')
    #     user_model = get_user_model()
    #     try:
    #         return user_model.objects.get(pk=user_id)
        
    #     except user_model.DoesNotExist:
    #         return None
        
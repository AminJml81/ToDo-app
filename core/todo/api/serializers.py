from rest_framework import serializers

from todo.models import Task
from accounts.models import User


class UserSerilizer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']


class TaskReadSerializer(serializers.ModelSerializer):
    user = UserSerilizer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_date', 'status', 'user']
    
    def get_status(self, obj):
        return obj.get_status_display()



class TaskCreateEditSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user']

    def get_status(self, obj):
        return obj.get_status_display()
    
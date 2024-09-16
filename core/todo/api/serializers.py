from rest_framework import serializers

from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

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


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user']

    def validate(self, validated_data):
        title = validated_data.get('title')
        if title:
            # if task title is getting updated or new task is created
            slug = slugify(title)
            if not slug:
                raise ValidationError({"title":f"Invalid title '{title}' !!!"})
            validated_data['slug'] = slug
        return validated_data
    

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        user = UserSerilizer(instance.user)
        representaion['user'] = UserSerilizer(instance.user).data
        return representaion
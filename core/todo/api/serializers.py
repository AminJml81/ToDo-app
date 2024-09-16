from rest_framework import serializers

from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from todo.models import Task
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']


class TaskReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    status = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['link','title', 'description', 'created_date', 'status', 'user']
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_link(self, obj):
        request = self.context.get('request')
        link = request.build_absolute_uri()
        if not 'v' in link.split('/')[-3]:
            # 'for list view add "id/" '
            link = link + str(obj.id) + '/'
        return link
    

class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    link = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['link', 'title', 'description', 'status', 'user']

    def get_link(self, obj):
        request = self.context.get('request')
        link = request.build_absolute_uri()
        if not 'v' in link.split('/')[-3]:
            # 'for list view add "id/" '
            link = link + str(obj.id) + '/'
        return link
    
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
        user = UserSerializer(instance.user).data
        representaion['user'] = user
        representaion['status'] = instance.get_status_display()
        return representaion
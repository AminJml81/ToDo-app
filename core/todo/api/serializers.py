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
        cleaned_link = self.clean_object_link(link, obj.id)
        return cleaned_link
    
    def clean_object_link(self, link, obj_id):
        if  len(link.split('?')) > 1:
            # discard query parameters from link
            link = link.split('?')[0]
        if 'v' in link.strip().split('/')[-2]:
            # 'add task id in list views
            # for list view -2 index is v(number) but for detail it is -3
            link = link + str(obj_id) + '/'
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
        cleaned_link = self.clean_object_link(link, obj.id)
        return cleaned_link
    
    def clean_object_link(self, link, obj_id):
        if 'page=' in link.split('?')[-1]:
            # discard page query parameter for single object link
            link = link.split('?')[0]
        if 'v' in link.strip().split('/')[-2]:
            # 'add task id in list views
            # for list view -2 index is v(number) but for detail it is -3
            link = link + str(obj_id) + '/'
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
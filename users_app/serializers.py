from rest_framework import serializers
from .models import CustomUser, SocialMedia, Blum, Tasks, Invitation


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['username', 'telegram_id', 'first_name', 'avatar', 'last_login']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
        

class SocialMedia(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['icon']


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['task_name', 'task_prize_amount', 'task_url', 'task_icon']


class BlumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blum
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['user', 'invite_link', 'invited_users']
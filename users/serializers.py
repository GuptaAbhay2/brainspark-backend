from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'brain_score',
                  'total_games', 'current_streak', 'longest_streak', 'created_at']
        read_only_fields = ['brain_score', 'total_games', 'current_streak',
                            'longest_streak', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        return User.objects.create(**validated_data)

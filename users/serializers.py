from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'telegram_chat_id')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            telegram_chat_id=validated_data.get('telegram_chat_id', '')
        )
        return user

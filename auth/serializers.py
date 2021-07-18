from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class MyUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'nickname',)
        read_only_fields = ('username',)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=20,
        min_length=5,
        required=True,
    )
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        return get_adapter().clean_username(username)

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'password': self.validated_data.get('password', ''),
        }

    @transaction.atomic
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()

        username = self.cleaned_data['username']
        nickname = self.cleaned_data['nickname']
        password = self.cleaned_data['password']

        user.username = username
        user.nickname = nickname
        user.set_password(password)

        user.save()

        return user

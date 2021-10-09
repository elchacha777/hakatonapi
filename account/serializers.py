from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .tasks import send_activation_sms
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

MyUser = get_user_model()


def validate_phone_number(phone_number):
    if MyUser.objects.filter(phone_number=phone_number).exists():
        raise serializers.ValidationError("Пользователь с данным номером уже существует")
    return phone_number


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'username', 'password', 'password_confirm')

    def validate_user_name(self, username):
        if MyUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Пользователь с данным именем уже существует")
        return username

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs


    def create(self, validated_data):
        user = MyUser.objects._create_user(**validated_data)
        send_activation_sms(str(user.phone_number), user.activation_code)
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'username': self.user.username})
        data.update({'phone_number': self.user.phonen_number})
        # and everything else you want to send in the response
        return data
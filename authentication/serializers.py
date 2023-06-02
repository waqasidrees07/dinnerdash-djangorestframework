from rest_framework import serializers
from .models import MyUser
import random
from django.core.mail import send_mail


class SignupSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(max_length=6, read_only=True)

    class Meta:
        model = MyUser
        fields = "__all__"

    def create(self, validated_data):
        # Generate a random verification code
        verification_code = int(random.randint(100000, 999999))

        # Create a new user
        user = MyUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            verification_code=verification_code
        )
        user.save()

        subject = 'Account Verification'
        message = f'Your verification code is: {verification_code}'
        send_mail(
            f'{subject}',
            f'{message}',
            'waqasidrees15@gmail.com',
            [f'{user.email}'],
            fail_silently=False,
        )
        return user



class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=20)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
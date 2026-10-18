from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['id','phone','password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create_user(
            phone = validated_data['phone'],
            password= validated_data['password']
        )

        return user


class PhoneTokenSerializer(TokenObtainPairSerializer):
    username_field = 'phone'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','user_id','firstname','lastname','username','bio']
        read_only_fields = ['id','user_id']


from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User,Profile,Avatar
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


class AvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id','image']
        read_only_fields = ['id']

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Razmer de doljen bit bolshe 5 МБ.')

        if value.content_type not in ['image/jpeg','image/png','image/webp',]:
            raise serializers.ValidationError('Razresheni tolko  JPG, PNG i WEBP.')

        return value






from rest_framework import serializers
from ..models import User

class SignupSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'password', 'password_confirm', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'nickname': {'required': True},
            }

    def validate(self, data):
        # 비밀번호 일치 검사
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def validate_email(self, value):
        # 이메일 중복 검사
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def validate_nickname(self, value):
        # 닉네임 중복 검사
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def create(self, validated_data):
        # 비밀번호 확인 필드 제거
        validated_data.pop('password_confirm', None)

        # 사용자 생성
        user = User.objects.create_user(
            nickname=validated_data['nickname'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
# apps/users/managers.py

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    커스텀 User 모델을 위한 Manager
    """

    def create_user(self, email=None, nickname=None, password=None, **extra_fields):
        """
        일반 사용자 생성
        """
        if not email and not nickname:
            raise ValueError('이메일 또는 닉네임 중 하나는 필수입니다.')

        if email:
            email = self.normalize_email(email)

        # 기본값 설정
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(
            email=email,
            nickname=nickname,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # 소셜 로그인 사용자

        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        """
        관리자 사용자 생성
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nickname, password, **extra_fields)

    def create_social_user(self, provider, provider_id, provider_email=None, **extra_fields):
        """
        소셜 로그인 사용자 생성
        """
        # 이미 연동된 소셜 계정이 있는지 확인
        from .models import SocialAccount

        try:
            social_account = SocialAccount.objects.get(
                provider=provider,
                provider_id=provider_id
            )
            return social_account.user
        except SocialAccount.DoesNotExist:
            pass

        # 이메일로 기존 사용자 찾기
        user = None
        if provider_email:
            try:
                user = self.get(email=provider_email)
            except self.model.DoesNotExist:
                pass

        # 새 사용자 생성 또는 기존 사용자 사용
        if not user:
            # 닉네임 자동 생성
            if not extra_fields.get('nickname'):
                base_nickname = f"{provider}_user"
                counter = 1
                nickname = base_nickname
                while self.filter(nickname=nickname).exists():
                    nickname = f"{base_nickname}_{counter}"
                    counter += 1
                extra_fields['nickname'] = nickname

            user = self.create_user(
                email=provider_email,
                password=None,  # 소셜 로그인 사용자는 비밀번호 없음
                **extra_fields
            )

        # 소셜 계정 연동 정보 생성
        SocialAccount.objects.create(
            user=user,
            provider=provider,
            provider_id=provider_id,
            provider_email=provider_email,
            extra_data=extra_fields.get('extra_data', {})
        )

        return user

    def get_by_email_or_nickname(self, identifier):
        """
        이메일 또는 닉네임으로 사용자 찾기
        """
        if '@' in identifier:
            return self.get(email=identifier)
        else:
            return self.get(nickname=identifier)
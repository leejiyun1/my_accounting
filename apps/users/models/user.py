# apps/users/models/user.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from ..managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    커스텀 User 모델
    소셜 로그인을 고려한 설계
    """

    nickname = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="사용자 닉네임"
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        null=True,
        blank=True,
        help_text="이메일 주소"
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="전화번호 (국제 형식)"
    )

    first_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="이름"
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="성"
    )

    profile_image = models.URLField(
        max_length=255,
        blank=True,
        help_text="프로필 이미지 URL"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="계정 활성화 상태"
    )

    is_email_verified = models.BooleanField(
        default=False,
        help_text="이메일 인증 여부"
    )

    is_phone_verified = models.BooleanField(
        default=False,
        help_text="전화번호 인증 여부"
    )

    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="마지막 로그인 시간"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="계정 생성 시간"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="계정 수정 시간"
    )

    # Django 기본 필드들
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # PermissionsMixin의 groups, user_permissions와 충돌 방지
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'  # 로그인 시 사용할 필드
    REQUIRED_FIELDS = ['nickname']  # createsuperuser 시 필요한 필드들

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'

    def __str__(self):
        return self.nickname or self.email or f"User {self.id}"

    @property
    def full_name(self):
        """전체 이름 반환"""
        return f"{self.last_name}{self.first_name}".strip()

    def has_usable_password(self):
        """소셜 로그인 사용자는 비밀번호가 없을 수 있음"""
        return super().has_usable_password()
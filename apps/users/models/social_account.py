# apps/users/models/social_account.py

from django.db import models
from django.utils import timezone
from .user import User


class SocialAccount(models.Model):
    """
    소셜 로그인 계정 연동 정보
    """

    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('kakao', 'Kakao'),
        ('naver', 'Naver'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='social_accounts',
        help_text="연동된 사용자"
    )

    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        help_text="소셜 로그인 제공자"
    )

    provider_id = models.CharField(
        max_length=100,
        help_text="소셜 제공자의 사용자 ID"
    )

    provider_email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        help_text="소셜에서 받은 이메일"
    )

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="소셜에서 받은 추가 정보"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="연동 생성 시간"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="연동 수정 시간"
    )

    class Meta:
        db_table = 'social_accounts'
        verbose_name = '소셜 계정'
        verbose_name_plural = '소셜 계정들'
        constraints = [
            models.UniqueConstraint(
                fields=['provider', 'provider_id'],
                name='unique_social_account'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'provider']),
        ]

    def __str__(self):
        return f"{self.user} - {self.provider}"
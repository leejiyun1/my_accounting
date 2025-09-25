# apps/finances/models/account.py

from django.db import models
from django.utils import timezone


class Account(models.Model):
    """
    계정과목 모델 (복식부기)
    """

    ACCOUNT_TYPE_CHOICES = [
        ('asset', '자산'),
        ('liability', '부채'),
        ('equity', '자본'),
        ('revenue', '수익'),
        ('expense', '비용'),
    ]

    user_id = models.BigIntegerField(
        help_text="사용자 ID (외래키 제약 없이 참조)"
    )

    account_code = models.CharField(
        max_length=10,
        help_text="계정과목 코드 (예: 1100, 4100)"
    )

    account_name = models.CharField(
        max_length=50,
        help_text="계정과목명 (예: 현금, 식비)"
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        help_text="계정과목 유형"
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="상위 계정과목"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="활성화 상태"
    )

    book_type = models.CharField(
        max_length=20,
        choices=[
            ('personal', '개인장부'),
            ('business', '사업장부')
        ]
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="생성 시간"
    )

    class Meta:
        db_table = 'accounts'
        verbose_name = '계정과목'
        verbose_name_plural = '계정과목들'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['account_code']),
        ]

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"
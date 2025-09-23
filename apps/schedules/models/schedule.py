# apps/schedules/models/schedule.py

from django.db import models
from django.utils import timezone
from .schedule_category import ScheduleCategory


class Schedule(models.Model):
    """
    일정 모델
    """

    STATUS_CHOICES = [
        ('scheduled', '예정'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    user_id = models.BigIntegerField(
        help_text="사용자 ID (외래키 제약 없이 참조)"
    )

    title = models.CharField(
        max_length=255,
        help_text="일정 제목"
    )

    description = models.TextField(
        blank=True,
        help_text="일정 설명"
    )

    start_datetime = models.DateTimeField(
        help_text="시작 일시"
    )

    end_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="종료 일시"
    )

    is_all_day = models.BooleanField(
        default=False,
        help_text="하루종일 일정 여부"
    )

    category = models.ForeignKey(
        ScheduleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="일정 카테고리"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        help_text="일정 상태"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="생성 시간"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="수정 시간"
    )

    class Meta:
        db_table = 'schedules'
        verbose_name = '일정'
        verbose_name_plural = '일정들'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['start_datetime']),
            models.Index(fields=['user_id', 'start_datetime']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_datetime.date()}"
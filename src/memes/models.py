from django.contrib.auth import get_user_model
from django.db import models

from appsettings.models import BaseModel

User = get_user_model()


class SourceChoices(models.TextChoices):
    USER = 'uploaded_by_user', 'Загружено пользователем'
    GENERATED = 'generated', 'Сгенерировано'


class MemePost(BaseModel):
    """Модель для хранения записи с мемом"""

    SourceChoices = SourceChoices

    image = models.ImageField(verbose_name='Изображение')
    description = models.CharField(verbose_name='Описание', max_length=300, blank=True)
    source = models.CharField(
        verbose_name='Источник мема', choices=SourceChoices.choices, max_length=20
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='memes',
        null=True,
    )
    likes = models.ManyToManyField(
        User, through='memes.MemeLike', related_name='liked_memes'
    )

    class Meta:
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'

    def __str__(self) -> str:
        return f'Мем {self.pk}. ({self.source})'


class MemeLike(BaseModel):
    """Модель для хранения записи о лайке мема пользователем"""

    meme = models.ForeignKey(
        MemePost,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'meme'], name='unique_likes')
        ]

    def __str__(self) -> str:
        return f'{self.user} лайкнул {self.meme}'

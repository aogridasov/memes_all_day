from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания', auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время последнего обновления', auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ['-updated_at']

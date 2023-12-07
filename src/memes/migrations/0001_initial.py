# Generated by Django 4.2 on 2023-12-06 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MemeLike',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Дата и время создания'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True, verbose_name='Дата и время последнего обновления'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
            },
        ),
        migrations.CreateModel(
            name='MemePost',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Дата и время создания'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True, verbose_name='Дата и время последнего обновления'
                    ),
                ),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                (
                    'description',
                    models.CharField(
                        blank=True, max_length=300, verbose_name='Описание'
                    ),
                ),
                (
                    'source',
                    models.CharField(
                        choices=[
                            ('uploaded_by_user', 'Загружено пользователем'),
                            ('generated', 'Сгенерировано'),
                        ],
                        max_length=20,
                        verbose_name='Источник мема',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='memes',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Автор',
                    ),
                ),
                (
                    'likes',
                    models.ManyToManyField(
                        related_name='liked_memes',
                        through='memes.MemeLike',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Мем',
                'verbose_name_plural': 'Мемы',
            },
        ),
        migrations.AddField(
            model_name='memelike',
            name='meme',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='memes.memepost'
            ),
        ),
        migrations.AddField(
            model_name='memelike',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddConstraint(
            model_name='memelike',
            constraint=models.UniqueConstraint(
                fields=('user', 'meme'), name='unique_likes'
            ),
        ),
    ]

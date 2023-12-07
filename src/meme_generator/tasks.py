import asyncio

from celery import shared_task

from meme_generator.generator import MemeGenerator


@shared_task
def generate_memes_task():
    """Генерируем мемы и сохраняем в БД"""

    asyncio.run(MemeGenerator.generate())

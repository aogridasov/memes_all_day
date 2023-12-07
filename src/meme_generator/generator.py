import aiohttp
from django.conf import settings

from memes.models import MemePost

from .jokeapi_requests import get_random_joke_text
from .memegen_requests import generate_meme_by_text
from .utils import ParseException


class MemeGenerator:
    def __init__(self):
        self.MEMES_TO_GENERATE = settings.MEMES_TO_GENERATE
        self.session = None

    @classmethod
    async def create(cls):
        """
        Метод для асинхронного создания экземпляра генератора
        """

        self = MemeGenerator()
        self.session = aiohttp.ClientSession()
        return self

    async def generate_meme(self) -> tuple:
        """Генерируем один мем"""

        text = await get_random_joke_text(self.session)
        meme_data = await generate_meme_by_text(self.session, text)
        return meme_data, text

    async def create_meme_objs(self):
        """Генерируем список с объектами мемов"""

        meme_objs = []
        loops_left = self.MEMES_TO_GENERATE * 2

        while len(meme_objs) < self.MEMES_TO_GENERATE and loops_left >= 0:
            try:
                image, text = await self.generate_meme()
                meme_obj = MemePost(
                    image=image,
                    description=text,
                    source=MemePost.SourceChoices.GENERATED,
                )
                meme_objs.append(meme_obj)

            except ParseException:
                pass
            loops_left -= 1

        return meme_objs

    @classmethod
    async def generate(cls):
        """Генерируем мемы и сохраняем в БД"""

        generator = await cls.create()
        memes = await generator.create_meme_objs()
        await MemePost.objects.abulk_create(memes)
        await generator.session.close()

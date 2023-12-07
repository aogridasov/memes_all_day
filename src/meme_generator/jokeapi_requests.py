from aiohttp import ClientSession

from .utils import base_request


async def get_random_joke_text(session: ClientSession):
    """
    Делаем запрос к jokeapi и возвращаем теткст случайной шутки.
    """

    excluded_flags = 'nsfw,religious,political,racist,sexist,explicit'
    url = f'https://v2.jokeapi.dev/joke/Any?blacklistFlags={excluded_flags}'
    joke_data = await base_request(session, url)
    joke_type = joke_data.get('type')

    if joke_type == 'single':
        return joke_data.get('joke')

    elif joke_type == 'twopart':
        setup = joke_data.get('setup')
        punchline = joke_data.get('delivery')

        if all([setup, punchline]):
            return setup + ' ' + punchline

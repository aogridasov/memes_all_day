from aiohttp import ClientSession

from .utils import base_request


async def generate_meme_by_text(session: ClientSession, text: str):
    """
    Делаем запрос к api.memegen.link и возвращаем
    мем с / по переданному тексту.
    """

    url = 'https://api.memegen.link/images/automatic'
    data = {'text': text, 'safe': True, 'redirect': True}
    return await base_request(session, url, 'POST', data)

from io import BytesIO

from aiohttp import ClientResponse, ClientSession, client_exceptions
from django.core.files import File, images


class ParseException(Exception):
    pass


async def decode_json(response: ClientResponse) -> dict:
    """
    Принимает ответ АПИ, возвращает
    словарь с ответом
    либо пустой словарь если расшифровка невозможна.
    """

    try:
        body = await response.json()
    except client_exceptions.ContentTypeError:
        body = {}
    return body


async def get_file_from_response(response: ClientResponse):
    """
    Возвращает объект картинки из ответа API.
    """

    img = await response.read()
    return images.ImageFile(file=File(BytesIO(img), name='meme'))


async def base_request(
    session: ClientSession, url: str, method: str = 'GET', data: dict = {}
):
    """Базовый запрос по преданным параметрам"""

    async with session.request(
        method=method,
        url=url,
        data=data,
    ) as response:
        response.raise_for_status()

        if response.content_type == 'application/json':
            return await decode_json(response)
        if response.content_type == 'image/jpeg':
            return await get_file_from_response(response)
        else:
            raise ParseException('Некорректный ответ API!')

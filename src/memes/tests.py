import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from .models import MemeLike, MemePost


class MemesTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user: User = User.objects.create_user(
            username='testuser', password='testpassword'
        )

        cls.user_meme: MemePost = MemePost.objects.create(
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            author=cls.user,
            description='user meme',
            source=MemePost.SourceChoices.USER,
        )

        cls.generated_meme: MemePost = MemePost.objects.create(
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            description='generated meme',
            source=MemePost.SourceChoices.GENERATED,
        )

        cls.meme_objs = [cls.user_meme, cls.generated_meme]

    def setUp(self):
        self.client.login(username='testuser', password='testpassword')

    def reverse_request(self, namespace: str, args: list = []) -> HttpResponse:
        """Выполняет HTTP GET-запрос к указанному namespace."""
        return self.client.get(reverse(namespace, args=args))

    def get_memes(self, response: HttpResponse) -> list:
        """Получает список мемов из контекста ответа."""
        return response.context.get('memepost_list', [])

    def test_index_status_code(self):
        """Проверяет, что страница главной страницы возвращает код 200."""
        response = self.reverse_request('memes:index')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_content(self):
        """Проверяет, что на главной странице отображаются все тестовые мемы."""
        response = self.reverse_request('memes:index')
        memes = self.get_memes(response)
        self.assertEqual(len(memes), len(self.meme_objs))
        for meme in self.meme_objs:
            with self.subTest(meme=meme):
                self.assertIn(meme, memes, 'Отсутствует мем!')

    def test_favorites_view(self):
        """Проверяет, что страница избранных возвращает код 200."""
        response = self.reverse_request('memes:favorites')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites.html')

    def test_favorites_content(self):
        """Проверяет, что на странице избранных отображаются только лайкнутые мемы."""
        response = self.reverse_request('memes:favorites')
        memes = self.get_memes(response)
        not_liked_memes = [meme for meme in self.meme_objs if meme.likes is None]

        self.assertEqual(len(memes), len(not_liked_memes))
        self.assertNotIn(self.user_meme, memes)
        MemeLike.objects.create(meme=self.user_meme, user=self.user)
        response = self.reverse_request('memes:favorites')
        memes = self.get_memes(response)
        self.assertIn(self.user_meme, memes)

    def test_my_uploads_view(self):
        """Проверяет, что страница загруженных пользователем возвращает код 200."""
        response = self.reverse_request('memes:my_memes')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_memes.html')

    def test_my_uploads_content(self):
        """Проверяет, что на странице загруженных отображаются только мемы пользователя."""
        response = self.reverse_request('memes:my_memes')
        memes = self.get_memes(response)
        user_memes = [meme for meme in self.meme_objs if meme.author == self.user]

        self.assertEqual(len(memes), len(user_memes))
        self.assertNotIn(self.generated_meme, memes)
        self.assertIn(self.user_meme, memes)

    def test_sign_up_view(self):
        """Проверяет, что страница регистрации возвращает код 200."""
        response = self.reverse_request('memes:signup')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')

    def test_like_meme_view(self):
        """Проверяет, что страница лайка мема успешно лайкает мем."""
        response = self.reverse_request('memes:like_meme', args=[self.user_meme.pk])
        self.assertEqual(response.status_code, 302)
        like_exists = MemeLike.objects.filter(
            meme=self.user_meme, user=self.user
        ).exists()
        self.assertTrue(like_exists)

    def test_unlike_meme_view(self):
        """Проверяет, что страница дизлайка мема успешно убирает лайк с мема."""
        response = self.reverse_request('memes:unlike_meme', args=[self.user_meme.pk])
        self.assertEqual(response.status_code, 302)
        like_exists = MemeLike.objects.filter(
            meme=self.user_meme, user=self.user
        ).exists()
        self.assertFalse(like_exists)

    def test_meme_upload_view(self):
        """Проверяет, что страница загрузки мема возвращает код 200."""
        response = self.reverse_request('memes:upload_meme')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_meme.html')

    def test_meme_create_view(self):
        """Проверяет, что страница создания мема успешно создает мем."""
        description = 'uploaded test meme'
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = 'test.gif'
        response = self.client.post(
            reverse('memes:meme_create'), {'description': description, 'image': img}
        )
        self.assertEqual(response.status_code, 302)
        uploaded_meme = MemePost.objects.filter(description=description).filter()
        self.assertTrue(uploaded_meme.exists())
        self.assertEqual(len(uploaded_meme), 1)

    def test_meme_delete_view(self):
        """Проверяет, что страница удаления мема успешно удаляет мем из базы данных."""
        response = self.reverse_request('memes:meme_delete', args=[self.user_meme.pk])
        self.assertEqual(response.status_code, 302)
        meme_exists = MemePost.objects.filter(pk=self.user_meme.pk).exists()
        self.assertFalse(meme_exists)

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User


class PostCacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username="test_user")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()

    def test_index_cache(self):
        post = Post.objects.create(
            text="Тестовый пост",
            author=PostCacheTest.user,
        )

        # Проверяем, что объект остался в кеше страницы после его
        # удаления из базы данных
        response_before_delete = self.guest_client.get(reverse("posts:index"))
        Post.objects.filter(pk=post.pk).delete()
        response_after_delete = self.guest_client.get(reverse("posts:index"))
        with self.subTest("Кеш не работает!"):
            self.assertEqual(
                response_before_delete.content,
                response_after_delete.content,
            )

        # Проверяем, что страница изменилась после очистки кеша
        cache.clear()
        response_after_clear = self.guest_client.get(reverse("posts:index"))
        with self.subTest("Очистка кеша не работает!"):
            self.assertNotEqual(
                response_before_delete.content,
                response_after_clear.content,
            )

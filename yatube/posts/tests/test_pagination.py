from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User
from ..views import POSTS_PER_PAGE


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username="test_user")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.posts = Post.objects.bulk_create(
            [
                Post(
                    author=cls.user,
                    text=f"Тестовый пост №{post_num}",
                    group=cls.group,
                )
                for post_num in range(11)
            ]
        )

    @classmethod
    def tearDownClass(cls):
        cls.group.delete()
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_paginator(self):
        """Проверка корректной работы paginator-а"""

        pages_with_paginator = [
            reverse("posts:index"),
            reverse(
                "posts:group_list",
                kwargs={"slug": PaginatorViewsTest.group.slug},
            ),
            reverse(
                "posts:profile",
                kwargs={"username": PaginatorViewsTest.user.username},
            ),
        ]
        for page in pages_with_paginator:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(
                    len(response.context["page_obj"]),
                    POSTS_PER_PAGE,
                )

from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Comment, Group, Post, User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.post_text = "Ооооооооочень длинный тестовый пост"
        cls.comment_text = "Ооооооооочень длинный тестовый комментарий"
        cls.group_data = {
            "title": "Тестовая группа",
            "slug": "test-slug",
            "description": "Тестовое описание",
        }

        cls.author = User.objects.create_user(username="author")
        cls.user = User.objects.create_user(username="test_user")
        cls.group = Group.objects.create(**cls.group_data)
        cls.post = Post.objects.create(
            author=cls.author,
            text=cls.post_text,
        )
        cls.comment = Comment.objects.create(
            text=cls.comment_text,
            post=cls.post,
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        cls.group.delete()
        cls.author.delete()
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_author = Client()
        self.authorized_author.force_login(URLTests.author)
        self.authorized_client = Client()
        self.authorized_client.force_login(URLTests.user)

    def test_urls_for_guest_users(self):
        """Проверка адресов, доступных для неавторизованного пользователя"""
        urls_response_codes = {
            "/": HTTPStatus.OK,
            f"/group/{URLTests.group.slug}/": HTTPStatus.OK,
            f"/posts/{URLTests.post.id}/": HTTPStatus.OK,
            f"/posts/{URLTests.post.id}/edit/": HTTPStatus.FOUND,
            f"/posts/{URLTests.post.id}/comment/": HTTPStatus.FOUND,
            "/create/": HTTPStatus.FOUND,
            "/unexisting_page/": HTTPStatus.NOT_FOUND,
            "/follow/": HTTPStatus.FOUND,
            f"/profile/{URLTests.author}/follow/": HTTPStatus.FOUND,
            f"/profile/{URLTests.author}/unfollow/": HTTPStatus.FOUND,
        }
        for url, response_code in urls_response_codes.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, response_code)

    def test_redirects_for_guest_users(self):
        """Проверка редиректов для неавторизованного пользователя"""
        urls_redirects = {
            f"/posts/{self.post.id}/edit/": f"/posts/{self.post.id}/",
            f"/posts/{self.post.id}/comment/": (
                f"/auth/login/?next=/posts/{self.post.id}/comment/"
            ),
            "/create/": "/auth/login/?next=/create/",
            "/follow/": "/auth/login/?next=/follow/",
            f"/profile/{URLTests.author}/follow/": (
                f"/auth/login/?next=/profile/{URLTests.author}/follow/"
            ),
            f"/profile/{URLTests.author}/unfollow/": (
                f"/auth/login/?next=/profile/{URLTests.author}/unfollow/"
            ),
        }
        for url, redirect_url in urls_redirects.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect_url)

    def test_urls_for_authorized_users(self):
        """Проверка адресов, доступных для авторизованного пользователя"""
        urls_response_codes = {
            "/": HTTPStatus.OK,
            f"/group/{URLTests.group.slug}/": HTTPStatus.OK,
            f"/posts/{URLTests.post.id}/": HTTPStatus.OK,
            f"/posts/{URLTests.post.id}/edit/": HTTPStatus.FOUND,
            f"/posts/{URLTests.post.id}/comment/": HTTPStatus.FOUND,
            "/create/": HTTPStatus.OK,
            "/follow/": HTTPStatus.OK,
            "/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for url, response_code in urls_response_codes.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, response_code)

    def test_redirects_for_authorized_users(self):
        """Проверка редиректов для авторизованного пользователя"""
        urls_redirects = {
            f"/posts/{self.post.id}/edit/": f"/posts/{self.post.id}/",
            f"/posts/{self.post.id}/comment/": f"/posts/{self.post.id}/",
        }
        for url, redirect_url in urls_redirects.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.authorized_client.get(url, follow=True)
                self.assertRedirects(response, redirect_url)

    def test_urls_for_post_authors(self):
        """Проверка адресов, доступных для автора сообщений"""
        urls_response_codes = {
            f"/posts/{URLTests.post.id}/edit/": HTTPStatus.OK,
        }
        for url, response_code in urls_response_codes.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.authorized_author.get(url)
                self.assertEqual(response.status_code, response_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        urls_templates = {
            "/": "posts/index.html",
            f"/group/{URLTests.group.slug}/": "posts/group_list.html",
            f"/posts/{URLTests.post.id}/": "posts/post_detail.html",
            "/create/": "posts/create_post.html",
            "/follow/": "posts/index.html",
        }
        for url, template in urls_templates.items():
            with self.subTest(url=url):
                response = self.authorized_author.get(url)
                self.assertTemplateUsed(response, template)

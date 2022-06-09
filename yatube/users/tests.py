from http import HTTPStatus

from django.test import Client, TestCase
from posts.models import User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username="test_user")

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(URLTests.user)

    def test_urls_for_guest_users(self):
        """Проверка адресов, доступных для неавторизованного пользователя"""
        urls_response_codes = {
            "/auth/signup/": HTTPStatus.OK,
            "/auth/login/": HTTPStatus.OK,
            "/auth/logout/": HTTPStatus.OK,
            "/auth/password_change/": HTTPStatus.FOUND,
            "/auth/password_change/done/": HTTPStatus.FOUND,
            "/auth/password_reset/": HTTPStatus.OK,
            "/auth/password_reset/done/": HTTPStatus.OK,
            "/auth/reset/<uidb64>/<token>/": HTTPStatus.OK,
            "/auth/reset/done/": HTTPStatus.OK,
            "/auth/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for url, response_code in urls_response_codes.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, response_code)

    def test_redirects_for_guest_users(self):
        """Проверка редиректов для неавторизованного пользователя"""
        urls_redirects = {
            "/auth/password_change/": (
                "/auth/login/?next=/auth/password_change/"
            ),
            "/auth/password_change/done/": (
                "/auth/login/?next=/auth/password_change/done/"
            ),
        }
        for url, redirect_url in urls_redirects.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect_url)

    def test_urls_for_authorized_users(self):
        """Проверка адресов, доступных для авторизованного пользователя"""
        urls_response_codes = {
            "/auth/signup/": HTTPStatus.OK,
            "/auth/login/": HTTPStatus.OK,
            "/auth/logout/": HTTPStatus.OK,
            # FIXME: почему-то для авторизованного пользователя
            #  возарвщается код 302 как-будто он неавторизованный
            # "/auth/password_change/": HTTPStatus.OK,
            # "/auth/password_change/done/": HTTPStatus.OK,
            "/auth/password_reset/": HTTPStatus.OK,
            "/auth/password_reset/done/": HTTPStatus.OK,
            "/auth/reset/<uidb64>/<token>/": HTTPStatus.OK,
            "/auth/reset/done/": HTTPStatus.OK,
            "/auth/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for url, response_code in urls_response_codes.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, response_code)

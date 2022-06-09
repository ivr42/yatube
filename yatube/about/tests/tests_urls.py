from http import HTTPStatus

from django.test import Client, TestCase


class URLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_for_guest_users(self):
        """Проверка адресов, доступных для всех пользователей"""
        urls_response_codes = {
            "/about/author/": HTTPStatus.OK,
            "/about/tech/": HTTPStatus.OK,
        }
        for url, response_code in urls_response_codes.items():
            with self.subTest(f"Проверяем {url}"):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, response_code)

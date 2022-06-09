from django.test import Client, TestCase
from django.urls import reverse
from posts.models import User


class TemplatesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username="test_user")

    def setUp(self):
        self.guest_client = Client()
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.csrf_client.force_login(TemplatesTests.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        urls_templates = {
            "/unexisting_page/": "core/404.html",
        }
        for url, template in urls_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_csrf_check_uses_correct_template(self):
        """
        Проверяем, что при создании поста без csrf-token
        используется нужный шаблон
        """

        form_data = {
            "text": "Новое тестовое сообщение",
        }

        response = self.csrf_client.post(
            reverse("post_create"),
            data=form_data,
            follow=True,
        )
        self.assertTemplateUsed(response, "core/403csrf.html")

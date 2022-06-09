from django.test import Client, TestCase


class URLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        urls_templates = {
            "/about/author/": "about/author.html",
            "/about/tech/": "about/tech.html",
        }
        for url, template in urls_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

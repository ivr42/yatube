from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        single_black_pixel_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00"
            b"\x01\x00\x80\x00\x00\x05\x04\x04"
            b"\x00\x00\x00\x2c\x00\x00\x00\x00"
            b"\x01\x00\x01\x00\x00\x02\x02\x44"
            b"\x01\x00\x3b"
        )
        SimpleUploadedFile(
            name="single_black_pixel.gif",
            content=single_black_pixel_gif,
            content_type="image/gif",
        )
        cls.user = User.objects.create_user(username="test_user")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.another_group = Group.objects.create(
            title="Ещё одна тестовая группа",
            slug="another-test-slug",
            description="И она тоже с описаним",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
            group=cls.group,
            image="posts/single_black_pixel.gif",
        )
        cls.page_names = [
            reverse("posts:index"),
            reverse("posts:group_list", kwargs={"slug": cls.group.slug}),
            reverse("posts:profile", kwargs={"username": cls.user.username}),
            reverse("posts:post_detail", kwargs={"post_id": cls.post.id}),
            reverse("posts:post_edit", kwargs={"post_id": cls.post.id}),
            reverse("post_create"),
        ]

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.group.delete()
        cls.another_group.delete()
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTest.user)

    def test_post_uses_correct_template(self):
        """Проверяем, что URL-адрес использует соответствующий шаблон."""

        templates = [
            "posts/index.html",
            "posts/group_list.html",
            "posts/profile.html",
            "posts/post_detail.html",
            "posts/create_post.html",
            "posts/create_post.html",
            "posts/index.html",
        ]
        for reverse_name, template in zip(PostPagesTest.page_names, templates):
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_has_correct_context(self):
        """Проверяем, что URL-адрес сформирован с правильным контекстом."""

        context_fields = [
            ("title", "page_obj", "index"),
            ("group", "page_obj"),
            ("username", "posts_count", "page_obj", "following"),
            ("post", "posts_count", "comments", "form"),
            ("title", "form", "groups", "is_edit"),
            ("title", "form", "groups", "is_edit"),
            ("title", "page_obj", "follow"),
        ]

        for reverse_name, context_fields in zip(
            PostPagesTest.page_names, context_fields
        ):
            response = self.authorized_client.get(reverse_name)
            for field in context_fields:
                with self.subTest(reverse_name=reverse_name):
                    self.assertIn(field, response.context)

    def test_post_with_group_works_correctly(self):
        """
        Проверяем, что сообщение с установленной группой есть
        на тех страницах, где должно быть и нет там,
        где его быть не должно
        """
        # Проверяем есть ли сообщение с заданной группой на страницах:
        # posts:index posts:group_list, posts:profile
        for reverse_name in PostPagesTest.page_names[:3]:
            with self.subTest(name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context.get("page_obj")), 1)

        # Проверяем, что сообщение с группой "Тестовая группа"
        # нет на странице группы "Ещё одна тестовая группа"
        name = reverse(
            "posts:group_list",
            kwargs={"slug": PostPagesTest.another_group.slug},
        )
        response = self.authorized_client.get(name)
        self.assertEqual(len(response.context.get("page_obj")), 0)

    def test_post_has_image(self):
        """Проверяем, что сообщение содержит картинку"""

        # Проверяем есть ли сообщение с картинкой на страницах:
        # posts:index posts:group_list, posts:profile
        for reverse_name in PostPagesTest.page_names[:3]:
            with self.subTest(name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_post = response.context.get("page_obj")[0]
                self.assertTrue(hasattr(first_post, "image"))

        # Проверяем есть ли сообщение с картинкой на странице:
        # posts:post_detail
        reverse_name = PostPagesTest.page_names[3]
        response = self.authorized_client.get(reverse_name)
        first_post = response.context.get("post")
        with self.subTest(name=reverse_name):
            self.assertTrue(hasattr(first_post, "image"))

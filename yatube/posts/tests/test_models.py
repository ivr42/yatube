from django.test import TestCase

from ..models import Comment, Follow, Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.post_text = "Ооооооооочень длинный тестовый пост"
        cls.comment_text = "Ооооооооочень длинный тестовый комментарий"
        cls.group_data = {
            "title": "Тестовая группа",
            "slug": "Тестовый слаг",
            "description": "Тестовое описание",
        }

        cls.user = User.objects.create_user(username="test")
        cls.author = User.objects.create_user(username="author")
        cls.group = Group.objects.create(**cls.group_data)
        cls.post = Post.objects.create(
            author=cls.user,
            text=cls.post_text,
        )
        cls.comment = Comment.objects.create(
            text=cls.comment_text,
            post=cls.post,
            author=cls.user,
        )
        cls.follow = Follow.objects.create(
            author=cls.author,
            user=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        cls.group.delete()
        cls.author.delete()
        cls.user.delete()
        super().tearDownClass()

    def test_group_has_correct_str(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        self.assertEqual(
            str(PostModelTest.group), PostModelTest.group_data["title"]
        )

    def test_post_has_correct_str(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(str(PostModelTest.post), PostModelTest.post_text[:15])

    def test_comment_has_correct_str(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(
            str(PostModelTest.comment), PostModelTest.comment_text[:15]
        )

    def test_follow_has_correct_str(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(
            str(PostModelTest.follow),
            f"{PostModelTest.author} followed by {PostModelTest.user}",
        )

    def test_models_have_correct_verbose_name(self):
        """Проверяем, что у моделей задано verbose_name"""

        models = (Group, Follow, Post, Comment)
        uncheck_fields = ("slug", "id")

        for model in models:
            for field in model._meta.get_fields(include_parents=False):
                if not hasattr(field, "verbose_name"):
                    continue
                if field.name in uncheck_fields:
                    continue
                with self.subTest(f"Модель {model.__class__.__name__}"):
                    self.assertNotEqual(
                        field.verbose_name,
                        field.name.replace("_", " "),  # default value
                        msg=(
                            f"У поля {field.name} не задано verbose_name,"
                            f"используется занчение по умолчанию"
                        ),
                    )

    def test_models_have_help_text(self):
        """Проверяем, что у моделей задан help_text"""

        models = (Group, Follow, Post, Comment)
        uncheck_fields = ("id",)

        for model in models:
            for field in model._meta.get_fields(include_parents=False):
                if not hasattr(field, "help_text"):
                    continue
                if field.name in uncheck_fields:
                    continue
                with self.subTest(f"Модель {model.__class__.__name__}"):
                    self.assertNotEqual(
                        field.help_text,
                        "",
                        msg=f"У поля {field.name} не задан help_text",
                    )

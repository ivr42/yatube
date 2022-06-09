import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateUpdateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username="test_user")
        cls.another_user = User.objects.create_user(username="another_user")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.another_group = Group.objects.create(
            title="Ещё одна тестовая группа",
            slug="another-group-slug",
            description="С ещё одним тестовым описанием",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cls.another_group.delete()
        cls.group.delete()
        cls.another_user.delete()
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateUpdateTest.user)
        self.non_author_client = Client()
        self.non_author_client.force_login(PostCreateUpdateTest.another_user)

    def test_create_post_authorized_user(self):
        """
        Проверяем, что авторизованный пользователь может
        создать сообщение
        """
        post_count = Post.objects.count()
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "Новое тестовое сообщение",
            "group": PostCreateUpdateTest.group.id,
            "image": uploaded,
        }
        response = self.authorized_client.post(
            reverse("post_create"),
            data=form_data,
            follow=True,
        )

        # Check if redirected
        with self.subTest():
            self.assertRedirects(
                response,
                reverse(
                    "posts:profile",
                    kwargs={"username": PostCreateUpdateTest.user.username},
                ),
            )

        # Check database object count
        with self.subTest():
            self.assertEqual(Post.objects.count(), post_count + 1)

        # Check if database object was created
        with self.subTest():
            self.assertTrue(
                Post.objects.filter(
                    text="Новое тестовое сообщение",
                    group=PostCreateUpdateTest.group.id,
                    image="posts/small.gif",
                ).exists()
            )

    def test_create_post_guest_user(self):
        """
        Проверяем, что неавторизованный пользователь не может
        создать сообщение
        """
        post_count = Post.objects.count()
        form_data = {
            "text": "Новое тестовое сообщение",
            "group": PostCreateUpdateTest.group.id,
        }
        self.guest_client.post(
            reverse("post_create"),
            data=form_data,
            follow=True,
        )

        # Check database object count
        with self.subTest():
            self.assertEqual(Post.objects.count(), post_count)

    def test_update_post_author(self):
        """Проверяем, что автор может изменять свои сообщения"""
        post_count = Post.objects.count()

        single_black_pixel_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00"
            b"\x01\x00\x80\x00\x00\x05\x04\x04"
            b"\x00\x00\x00\x2c\x00\x00\x00\x00"
            b"\x01\x00\x01\x00\x00\x02\x02\x44"
            b"\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile(
            name="single_black_pixel.gif",
            content=single_black_pixel_gif,
            content_type="image/gif",
        )
        form_data = {
            "text": "Сообщение изменено!",
            "group": PostCreateUpdateTest.another_group.id,
            "image": uploaded,
        }
        response = self.authorized_client.post(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": PostCreateUpdateTest.post.id},
            ),
            data=form_data,
            follow=True,
        )

        # Check if redirected
        with self.subTest():
            self.assertRedirects(
                response,
                reverse(
                    "posts:post_detail",
                    kwargs={"post_id": PostCreateUpdateTest.post.id},
                ),
            )

        # Check database object count
        with self.subTest():
            self.assertEqual(Post.objects.count(), post_count)

        # Check if message changed in database
        chaged_post = Post.objects.get(id=PostCreateUpdateTest.post.id)
        with self.subTest():
            self.assertEqual(chaged_post.text, form_data.get("text"))
        with self.subTest():
            self.assertEqual(chaged_post.group.id, form_data.get("group"))
        with self.subTest():
            self.assertEqual(chaged_post.image, "posts/single_black_pixel.gif")

    def test_update_post_non_author_user(self):
        """
        Проверяем, что авторизованный пользователь, но не автор
        поста, не может изменять сообщение
        """
        post_count = Post.objects.count()
        form_data = {
            "text": "Сообщение изменено!",
            "group": PostCreateUpdateTest.another_group.id,
        }
        self.non_author_client.post(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": PostCreateUpdateTest.post.id},
            ),
            data=form_data,
            follow=True,
        )

        # Check database object count
        with self.subTest():
            self.assertEqual(Post.objects.count(), post_count)

        # Check if message changed in database
        with self.subTest():
            chaged_post = Post.objects.get(id=PostCreateUpdateTest.post.id)
            self.assertNotEqual(chaged_post.text, form_data.get("text"))
            self.assertNotEqual(chaged_post.group, form_data.get("group"))

    def test_update_post_guest_user(self):
        """
        Проверяем, что неавторизованный пользователь не может
        изменять сообщение
        """
        post_count = Post.objects.count()
        form_data = {
            "text": "Сообщение изменено!",
        }
        self.guest_client.post(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": PostCreateUpdateTest.post.id},
            ),
            data=form_data,
            follow=True,
        )

        # Check database object count
        with self.subTest():
            self.assertEqual(Post.objects.count(), post_count)

        # Check if message changed in database
        with self.subTest():
            chaged_post = Post.objects.get(id=PostCreateUpdateTest.post.id)
            self.assertNotEqual(chaged_post.text, form_data.get("text"))
            self.assertNotEqual(chaged_post.group.id, form_data.get("group"))

    def test_create_comment_guest_user(self):
        """Проверяем, что гость не может создать комментарий"""

        post_comments_count_before = Comment.objects.filter(
            post=PostCreateUpdateTest.post,
        ).count()

        form_data = {
            "text": "Комментарий от неавторизованного пользователя",
        }

        self.guest_client.post(
            reverse(
                "posts:add_comment",
                kwargs={"post_id": PostCreateUpdateTest.post.id},
            ),
            data=form_data,
        )

        # Check database object count
        post_comments_count_after = Comment.objects.filter(
            post=PostCreateUpdateTest.post,
        ).count()
        with self.subTest():
            self.assertEqual(
                post_comments_count_after, post_comments_count_before
            )

    def test_create_comment_authorized_user(self):
        """
        Проверяем, что авторизованный пользователь может создать комментарий
        """
        post_comments_count_before = Comment.objects.filter(
            post=PostCreateUpdateTest.post,
        ).count()

        form_data = {
            "text": "Комментарий от авторизованного пользователя",
        }

        self.authorized_client.post(
            reverse(
                "posts:add_comment",
                kwargs={"post_id": PostCreateUpdateTest.post.id},
            ),
            data=form_data,
        )

        # Check database object count
        post_comments_count_after = Comment.objects.filter(
            post=PostCreateUpdateTest.post,
        ).count()
        with self.subTest(
            "Количество комментариев поста в базе данных не изменилось"
        ):
            self.assertEqual(
                post_comments_count_after, post_comments_count_before + 1
            )

        # Check comment exists in database
        with self.subTest("Комментария нет в базе данных"):
            self.assertTrue(
                Comment.objects.filter(
                    post=PostCreateUpdateTest.post,
                    text=form_data.get("text"),
                ).exists()
            )

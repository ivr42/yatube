from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Follow, Post, User


# turn off cache
@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
)
class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # создать автора
        cls.author = User.objects.create_user(username="author")
        # создать подписчика
        cls.follower = User.objects.create_user(username="follower")
        # создать пользователя без подписки
        cls.user = User.objects.create_user(username="test_user")
        # создать пост
        cls.post = Post.objects.create(
            author=cls.author,
            text="Тестовый пост",
        )

    @classmethod
    def tearDownClass(cls):
        cls.author.delete()
        cls.follower.delete()
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(FollowTest.user)
        self.author_client = Client()
        self.author_client.force_login(FollowTest.author)
        self.follower_client = Client()
        self.follower_client.force_login(FollowTest.follower)

    def test_guest_user_cant_follow(self):
        """Проверить, что гость не может подписываться на авторов"""

        followers_count_before = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        self.guest_client.get(
            "posts:profile_follow",
            username=FollowTest.author,
        )

        followers_count_after = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        self.assertEqual(followers_count_before, followers_count_after)

    def test_authorized_user_can_follow_unfollow(self):
        """Проверить, что авторизованный пользователь может подписываться"""
        followers_count_before = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        # Подписываемся
        self.follower_client.get(
            reverse(
                "posts:profile_follow", kwargs={"username": FollowTest.author}
            )
        )

        followers_count_after1 = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        with self.subTest():
            self.assertEqual(
                followers_count_after1, followers_count_before + 1
            )

        with self.subTest():
            self.assertTrue(
                Follow.objects.filter(
                    author=FollowTest.author,
                    user=FollowTest.follower,
                ).exists()
            )

        # Отписываемся
        self.follower_client.get(
            reverse(
                "posts:profile_unfollow",
                kwargs={"username": FollowTest.author},
            )
        )

        followers_count_after2 = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        with self.subTest():
            self.assertEqual(followers_count_after2, followers_count_before)

    def test_user_can_follow_only_ones(self):
        """
        Проверить, что создаётся только одна подписка
        если кто-то подпишется дважды на одного и того же
        автора
        """
        followers_count_before = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        # Подписываемся
        self.follower_client.get(
            reverse(
                "posts:profile_follow", kwargs={"username": FollowTest.author}
            )
        )

        # Подписываемся ещё раз
        self.follower_client.get(
            reverse(
                "posts:profile_follow", kwargs={"username": FollowTest.author}
            )
        )

        followers_count_after = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        with self.subTest():
            self.assertEqual(followers_count_after, followers_count_before + 1)

        follower_count = Follow.objects.filter(
            author=FollowTest.author,
            user=FollowTest.follower,
        ).count()

        with self.subTest():
            self.assertEqual(follower_count, 1)

    def test_user_cant_follow_themself(self):
        """Проверить, что пользователь не может подписаться сам на себя"""

        followers_count_before = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        # Подписываемся сами на себя
        self.author_client.get(
            reverse(
                "posts:profile_follow", kwargs={"username": FollowTest.author}
            )
        )

        followers_count_after = Follow.objects.filter(
            author=FollowTest.author
        ).count()

        with self.subTest():
            self.assertEqual(followers_count_after, followers_count_before)

    def test_user_have_followed_authors_posts(self):
        """Проверить, что у подписчика есть посты автора в ленте"""

        response1 = self.follower_client.get(reverse("posts:follow_index"))

        # Подписываемся
        self.follower_client.get(
            reverse(
                "posts:profile_follow", kwargs={"username": FollowTest.author}
            )
        )

        response2 = self.follower_client.get(reverse("posts:follow_index"))

        self.assertNotEqual(response2.content, response1.content)

    def test_no_follow_no_posts(self):
        """
        Проверить, что если пользователь не подписан на автора,
        то у него нет в ленте его постов
        """
        # Запрашиваем страницу follow_index под пользователем user
        response1 = self.authorized_client.get(reverse("posts:follow_index"))

        # Подписываемся пользователем follower
        self.follower_client.get(
            reverse(
                "posts:profile_follow", kwargs={"username": FollowTest.author}
            )
        )

        # Запрашиваем страницу follow_index под пользователем user
        response2 = self.authorized_client.get(reverse("posts:follow_index"))

        self.assertEqual(response2.content, response1.content)

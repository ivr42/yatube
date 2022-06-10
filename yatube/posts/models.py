from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name="Название сообщества",
        help_text="Введите название сообщества",
        max_length=200,
    )
    slug = models.SlugField(
        unique=True,
        help_text="Задайте slug",
    )
    description = models.TextField(
        verbose_name="Описание сообщества",
        help_text="Введите описание сообщества",
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name="Текст сообщения",
        help_text="Введите текст сообщения",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор сообщения",
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="Автор сообщения: автоматическое поле",
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Сообщество",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        help_text="Укажите сообщество",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="posts/",
        blank=True,
        help_text="Добавьте картинку (по желанию)",
    )
    created = models.DateTimeField(
        verbose_name="Дата и время публикации",
        auto_now_add=True,
        help_text="Дата и время публикации: автоматическое поле",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Введите текст комментария",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор комментария",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Автор комментария: автоматическое поле",
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Комментируемый пост",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Ссылка на пост, к которому оставлен комментарий",
    )
    created = models.DateTimeField(
        verbose_name="Дата и время публикации",
        auto_now_add=True,
        help_text="Дата и время публикации: автоматическое поле",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор сообщений",
        on_delete=models.CASCADE,
        related_name="following",
        help_text="Укажите автора сообщений,"
        "на которого хотите подписаться/отписаться",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
        related_name="follower",
        help_text="Подписчик: автоматическое поле",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.author} followed by {self.user}"

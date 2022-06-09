from django.db import models


class BaseModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""

    created = models.DateTimeField(
        verbose_name="Дата и время публикации",
        auto_now_add=True,
        help_text="Дата и время публикации: автоматическое поле",
    )
    text = models.TextField()

    class Meta:
        ordering = ["-created"]
        abstract = True

    def __str__(self):
        return self.text[:15]

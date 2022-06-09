# Generated by Django 2.2.16 on 2022-06-05 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_post_group"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-pub_date"],
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
            },
        ),
        migrations.AlterField(
            model_name="group",
            name="description",
            field=models.TextField(
                help_text="Введите описание сообщества",
                verbose_name="Описание сообщества",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="slug",
            field=models.SlugField(help_text="Задайте slug", unique=True),
        ),
        migrations.AlterField(
            model_name="group",
            name="title",
            field=models.CharField(
                help_text="Введите название сообщества",
                max_length=200,
                verbose_name="Название сообщества",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                help_text="Автор сообщения: автоматическое поле",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор сообщения",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="group",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите сообщество",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="posts.Group",
                verbose_name="Сообщество",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="Дата публикации: автоматическое поле",
                verbose_name="Дата публикации",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(
                help_text="Введите текст сообщения",
                verbose_name="Текст сообщения",
            ),
        ),
    ]

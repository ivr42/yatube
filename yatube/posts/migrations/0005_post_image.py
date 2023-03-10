# Generated by Django 2.2.16 on 2022-06-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_auto_20220605_1454"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Добавьте картинку (по желанию)",
                upload_to="posts/",
                verbose_name="Картинка",
            ),
        ),
    ]

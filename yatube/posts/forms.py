from django.forms import ModelForm

from .models import Comment, Post


# TODO: Написать сообщения об ошибках
#       на русском языке
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group", "image")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

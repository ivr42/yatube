from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Group, Post


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class PostSerializer(ModelSerializer):
    group = SlugRelatedField(
        required=False,
        allow_null=True,
        slug_field="slug",
        queryset=Group.objects.all(),
    )

    class Meta:
        model = Post
        fields = ("id", "text", "author", "image", "created", "group")

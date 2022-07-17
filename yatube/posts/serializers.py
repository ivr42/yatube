from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Group, Post, Tag, TagPost


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class PostSerializer(ModelSerializer):
    tag = TagSerializer(many=True, required=False, allow_null=True)
    group = SlugRelatedField(
        required=False,
        allow_null=True,
        slug_field="slug",
        queryset=Group.objects.all(),
    )

    class Meta:
        model = Post
        fields = ("id", "text", "author", "image", "created", "group", "tag")

    def create(self, validated_data):
        if "tag" not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post

        tags = validated_data.pop("tag")

        post = Post.objects.create(**validated_data)

        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            TagPost.objects.create(tag=current_tag, post=post)
        return post

    def update(self, instance, validated_data):
        if "tag" in self.initial_data:
            tags = validated_data.pop("tag") or []
            instance.tag.set(
                [Tag.objects.get_or_create(**tag)[0] for tag in tags]
            )
        return super().update(instance, validated_data)

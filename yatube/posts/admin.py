from django.contrib import admin

from .models import Comment, Follow, Group, Post, Tag, TagPost


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "created", "author", "post")
    list_editable = (
        "author",
        "post",
    )
    search_fields = ("text",)
    list_filter = ("created", "author")
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "user")
    list_editable = (
        "author",
        "user",
    )
    list_filter = ("user", "author")


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "created", "author", "group")
    list_editable = ("group",)
    search_fields = ("text",)
    list_filter = ("created", "author", "group")
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "slug", "title", "description")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_editable = ("name",)
    search_fields = ("name",)


class TagPostAdmin(admin.ModelAdmin):
    list_display = ("pk", "tag", "post")
    list_editable = ("tag", "post")
    search_fields = ("tag",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagPost, TagPostAdmin)

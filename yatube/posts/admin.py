from django.contrib import admin

from .models import Group, Post


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


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)

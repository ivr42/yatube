from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from posts.views import post_create

urlpatterns = [
    path("", include("posts.urls", namespace="posts")),
    path("about/", include("about.urls", namespace="about")),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("create/", post_create, name="post_create"),
]

handler404 = "core.views.page_not_found"

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

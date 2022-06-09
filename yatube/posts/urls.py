from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.index, name="index"),
    # Posts in certain community
    path("group/<slug:slug>/", views.group_posts, name="group_list"),
    # User profile and his posts
    path("profile/<str:username>/", views.profile, name="profile"),
    # Single post view
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    # Edit post
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    # Add comment
    path(
        "posts/<int:post_id>/comment/", views.add_comment, name="add_comment"
    ),
    path("follow/", views.follow_index, name="follow_index"),
    path(
        "profile/<str:username>/follow/",
        views.profile_follow,
        name="profile_follow",
    ),
    path(
        "profile/<str:username>/unfollow/",
        views.profile_unfollow,
        name="profile_unfollow",
    ),
]

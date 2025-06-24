from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    # path("", views.post, name="post_list"),  # Default post listing view
    path("post_list/", views.manage_posts, name="post_list"),
    path("list_posts/", views.list_posts, name="list_posts"),
    path("view_post/<int:post_id>/", views.post_detail, name="view_post"),
    path("post_comment/<int:post_id>/", views.post_comment, name="post_comment"),
    path("category_list/", views.category_list, name="category_list"),
    path("add_category/", views.add_category, name="add_category"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
]

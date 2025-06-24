from django.urls import path
from .import views
app_name='users'
urlpatterns = [
    # path('',views.main_page,name='blog'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path("admin/login/", views.CustomAdminLoginView.as_view(), name="custom_admin_login"),
    path('logout/',views.user_logout,name='logout'),
    path("author_dashboard/", views.author_dashboard, name="author_dashboard"),
    # path("author_dashboard/overview/", views.author_dashboard_overview, name="author_dashboard_overview"),
    path("author_dashboard/my_posts/", views.author_dashboard_my_posts, name="author_dashboard_my_posts"),
    path("author_dashboard/create_post/", views.author_dashboard_create_post, name="author_dashboard_create_post"),
    # path("author_dashboard/post_analytics/", views.author_dashboard_post_analytics, name="author_dashboard_post_analytics"),
    path("author_dashboard/profile_settings/", views.author_dashboard_profile_settings, name="author_dashboard_profile_settings"),
    path("author_dashboard/post_detail/<int:post_id>/", views.author_dashboard_post_detail, name="author_dashboard_post_detail"),
    path("author_dashboard/edit_post/<int:post_id>/", views.author_dashboard_edit_post, name="author_dashboard_edit_post"),
    path("author_dashboard/delete_post/<int:post_id>/", views.author_dashboard_delete_post, name="author_dashboard_delete_post"),
    path("comment/delete/<int:comment_id>/",views.delete_comment, name="delete_comment"),
    path('',views.home_page,name='home'),
    path('superuser_dashboard/', views.admin_dashboard, name='superuser_dashboard'),
    path('superuser_dashboard/users/', views.users_list, name='users_list'),
    path('superuser_dashboard/authors/', views.author_list, name='author_list'),
    path('superuser_dashboard/posts/', views.post_list, name='post_list'),
    path('superuser_dashboard/post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path("posts/delete/<int:post_id>/", views.superuser_delete_post, name="superuser_delete_post"),
    path('toggle-user/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path("category/", views.category_posts, name="category_posts"),
]


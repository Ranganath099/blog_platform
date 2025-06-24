from django.db import models
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Published", "Published"),
    ]
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Draft")
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")  # Added category field

    def __str__(self):
        return self.title

# Comment section anyone can comment the post by login.

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Any user can comment
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")  # Links to Post
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    def is_reply(self):
        return self.parent is not None
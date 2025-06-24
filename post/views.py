from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post,Comment,Category
from .forms import PostForm,CommentForm, CategoryForm   # Create a PostForm and CommentForm
from django.http import HttpResponseForbidden
from django.urls import reverse
from users.urls import urlpatterns

@login_required
def create_post(request):
    # Ensure only authors and super admins can create posts
    if not request.user.has_blog_edit_permission():
        messages.error(request, "You do not have permission to create posts.")
        return redirect("post:post_list")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the logged-in user as the author
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("users:author_dashboard")
    else:
        form = PostForm()

    return render(request, "post/create_post.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Allow the post author or a superuser to edit the post
    # if post.author != request.user and not request.user.is_superuser:
    #     messages.error(request, "You do not have permission to edit this post.")
    #     return redirect("post:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("users:author_dashboard")
    else:
        form = PostForm(instance=post)

    return render(request, "post/edit_post.html", {"form": form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Allow the post author or a superuser to delete the post
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect("post:post_list")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")

        # Redirect based on user role
        if request.user.is_superuser:
            return redirect(reverse("users:superuser_dashboard"))  # Redirect to superuser dashboard
        else:
            return redirect(reverse("post:post_list"))  # Redirect to author's post list

    return render(request, "post/delete_post.html", {"post": post})


@login_required
def manage_posts(request):
    # If the user is a superuser, show all posts
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        # Show only the posts by the logged-in author
        posts = Post.objects.filter(author=request.user)

    return render(request, "post/post_list.html", {"posts": posts})
@login_required
def list_posts(request):
    # Fetch posts created by authors
    posts = Post.objects.filter(author__role="author").exclude(id=None)
    for post in posts:
        post.top_level_comments = post.comments.filter(parent__isnull=True)

    # Render the list of posts to the template
    return render(request, "post/list_posts.html", {"posts": posts})

from django.shortcuts import render, get_object_or_404
from .models import Post

@login_required
def post_detail(request, post_id):
    
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  #  Fetch comments using related_name="comments"
    form = CommentForm()
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to view this post.")
        return redirect('users:')
    if request.method == "POST":
        post.view()
        messages.success(request, "Post deleted successfully!")

        # Redirect based on user role
        if request.user.is_superuser:
            return redirect(reverse("users:superuser_dashboard"))  # Redirect to superuser dashboard
        else:
            return redirect(reverse("users:authors_dashboard"))  # Redirect to author's post list


    # Redirect based on user role
    return render(request, 'post/post_detail.html', {'post': post, 'comments': comments, 'form': form})

# Comment the post View.

@login_required
def post_comment(request, post_id):
    """Show post details and handle comment submissions."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent__isnull=True).order_by("-created_at")
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            
            # Check if this is a reply to another comment
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment  # Set parent comment
            
            comment.save()
            return redirect(request.META.get("HTTP_REFERER", f"/post/{post.id}/"))  # Stay on the post page

    else:
        form = CommentForm()

    return render(request,"post/post_detail.html",{"post": post, "comments": comments, "form": form},)

@login_required
def delete_comment(request, comment_id):
    """Allow only authors and superusers to delete comments."""
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id  # Store post ID before deleting

    if request.method == "POST":
        if request.user == comment.user or request.user.is_superuser or request.user.role == "author":
            comment.delete()
            return redirect(reverse("post:list_posts"))

  # Redirect back to the post
        else:
            return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    return redirect("post:post_detail", post_id=post_id)
def category_list(request):
   categories = Category.objects.all()  # ✅ Get all categories from the database
   return render(request, "category_list.html", {"categories": categories})

from django.shortcuts import render, redirect
from post.models import Category
from .forms import CategoryForm

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post:add_category")  # Redirect to the same page

    else:
        form = CategoryForm()

    categories = Category.objects.all()  # Fetch all categories

    return render(request,"add_category.html",{"form": form, "categories": categories},)

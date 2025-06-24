from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout,get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailOrPhoneLoginForm, AuthorProfileForm
from .models import AuthorProfile,CustomUser
from post.models import Post, Comment, Category
from django.db.models import Count
from post.forms import PostForm
from django.contrib.admin.views.decorators import staff_member_required 
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in.")
            login(request, user, backend="users.backends.EmailOrPhoneBackend")
            return redirect("users:login")  
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

User = get_user_model()  # Ensure we use the custom user model
def user_login(request):
    if request.method == "POST":
        form = EmailOrPhoneLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=identifier, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect("users:superuser_dashboard")
                elif user.role == "author":
                    return redirect("users:author_dashboard")
                else:
                    return redirect("post:list_posts")
            else:
                form.add_error(None, "Invalid email/phone number or password")
    else:
        form = EmailOrPhoneLoginForm()
    
    return render(request, "login.html", {"form": form})


class CustomAdminLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return "/users/superuser_dashboard/"  # Redirect superuser to dashboard
        return super().get_success_url()


@login_required
def author_profile(request):
    # Get the author profile for the logged-in user
    profile, created = AuthorProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AuthorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:author_dashboard')  # Redirect to the author's dashboard
    else:
        form = AuthorProfileForm(instance=profile)
    return render(request, 'dashboard/author/author_profile.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("users:home")

@login_required(login_url="/users/login")
def author_dashboard(request):
    if request.user.role != "author":  
        messages.error(request, "You do not have permission to access this page.")
        return redirect("users:users_home")

    # return render(request, "dashboard/author/author_overview.html")

# @login_required
# def author_dashboard_overview(request):
    author_posts = request.user.post_set.all()
    published_posts = author_posts.filter(status="Published").count()
    draft_posts = author_posts.filter(status="Draft").count()
    total_posts = author_posts.count()
    total_views = author_posts.aggregate(total_views=Count("views"))["total_views"] or 0

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_post_counts = [author_posts.filter(created_at__month=i + 1).count() for i in range(12)]

    context = {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
        "total_views": total_views,
        "months": months,
        "monthly_post_counts": monthly_post_counts,
    }

    return render(request, "dashboard/author/author_overview.html", context)

@login_required
def author_dashboard_my_posts(request):
    posts = request.user.post_set.all()
    return render(request, "dashboard/author/post_list.html", {"posts": posts})

@login_required
def author_dashboard_create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        form.save_m2m()
        return redirect("users:author_dashboard_my_posts")

    return render(request, "dashboard/author/post_form.html", {"form": form})

@login_required
def author_dashboard_edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:author_dashboard_my_posts")

    return render(request, "dashboard/author/post_form.html", {"form": form, "post": post})

@login_required
def author_dashboard_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect("users:author_dashboard_my_posts")

@login_required
def author_dashboard_profile_settings(request):
    profile, created = AuthorProfile.objects.get_or_create(user=request.user)
    form = AuthorProfileForm(instance=profile)

    if request.method == "POST":
        form = AuthorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("users:author_dashboard_profile_settings")

    return render(request, "dashboard/author/author_profile.html", {"form": form, "profile": profile})

@login_required
@login_required
def author_dashboard_post_detail(request, post_id):
    """Display a post with comments and handle new comment submissions in the author's dashboard."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    comments = post.comments.filter(parent__isnull=True).order_by("-created_at")

    if request.method == "POST":
        comment_text = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        if comment_text:
            comment = Comment(post=post, user=request.user, content=comment_text)

            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment  # Set parent if it's a reply

            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect("users:author_dashboard_post_detail", post_id=post.id)

    return render(request, "dashboard/author/post_detail.html", {"post": post, "comments": comments})

@login_required
def delete_comment(request, comment_id):
    """Allow comment deletion if the user is the comment owner, a superuser, or the post author."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post  # Get the post related to the comment

    # Allow comment owner, superuser, or the post's author to delete it
    if request.user == comment.user or request.user.is_superuser or request.user == post.author:
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect("users:author_dashboard_post_detail", post_id=post.id)

def main_page(request):
    return render(request,'base.html')
def home_page(request):
    posts = Post.objects.filter(status="Draft").order_by("-created_at")[:6]  # Show latest 6 posts
    return render(request, "home.html", {"posts": posts})


# Custom decorator to ensure only superusers can access the view
# Ensure only superusers can access
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='/users/login/')(view_func)

#  Main Dashboard Layout
@superuser_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return render(request, "dashboard/superuser/access_denied.html")  # Restrict access

    # User stats
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    # Author & Post stats
    active_authors = AuthorProfile.objects.filter(user__is_active=True).count()
    total_posts = Post.objects.count()

    context = {
        "view": "overview",  # Ensure the correct view is passed for template logic
        "total_users": total_users,
        "active_users": active_users,
        "active_authors": active_authors,
        "total_posts": total_posts,
    }
    return render(request, 'dashboard/superuser/superuser_overview.html',context)


# Users List
@superuser_required
def users_list(request):
    users = CustomUser.objects.filter(role="user", is_superuser=False)
    return render(request, 'dashboard/superuser/users_list.html', {'users': users})


# Authors List
@superuser_required
def author_list(request):
    authors = CustomUser.objects.filter(role="author", is_superuser=False)
    return render(request, 'dashboard/superuser/author_list.html', {'authors': authors})


#  Posts List
@superuser_required
def post_list(request):
    category_name = request.GET.get("category_name")  # Get selected category name from request
    categories = Category.objects.all()  # Fetch all categories

    if category_name:
        posts = Post.objects.filter(category__name=category_name).select_related("author")
    else:
        posts = Post.objects.select_related("author").all()  # Get all posts if no category is selected

    return render(request,"dashboard/superuser/post_list.html",{"posts": posts, "categories": categories, "selected_category": category_name},)

#  View Post Details + Comments
@superuser_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by("-created_at")
   # Handling comment deletion
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")  # Get comment ID from form
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user.is_superuser:  # Ensure only superusers can delete
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this comment.")

        return redirect('users:post_detail', post_id=post.id)  # Redirect to refresh page

    return render(request, 'dashboard/superuser/post_detail.html', {'post': post, 'comments': comments})

@superuser_required
def superuser_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        post.delete()
        return redirect("users:post_list")  # Redirect after deletion

    return render(request, "dashboard/superuser/post_delete.html", {"post": post})


# Toggle User Activation
@login_required
@superuser_required
def toggle_user_active(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()

    messages.success(request, f"User {user.email or user.phone_number} status updated.")
    return redirect(request.META.get('HTTP_REFERER', 'superuser_dashboard'))


#  Delete User
@login_required
@superuser_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()

    messages.success(request, "User deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'superuser_dashboard'))

def category_posts(request, category_name=None):
    categories = Category.objects.all()  # Get all categories for the dropdown

    if category_name:
        category = get_object_or_404(Category, name=category_name)  # Get selected category by name
        posts = Post.objects.filter(category=category)  # Filter posts by category
    else:
        posts = Post.objects.all()  # Show all posts if no category is selected

    return render(request, "category_posts.html", {"posts": posts, "categories": categories, "selected_category": category_name})
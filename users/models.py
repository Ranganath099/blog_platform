# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# # Custom Manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         """
#         Creates and saves a User with either an email or a phone number.
#         """
#         if not username:
#             raise ValueError("The Email or Phone number field is required")

#         if "@" in username:
#             extra_fields["email"] = self.normalize_email(username)
#             extra_fields["phone_number"] = None
#         else:
#             extra_fields["phone_number"] = username
#             extra_fields["email"] = None

#         user = self.model(**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         """
#         Creates and saves a superuser with all permissions.
#         """
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("role", "super_admin")
#         if not email:
#             raise ValueError("Superuser must have an email or phone number")

#         return self.create_user(username=email, password=password, **extra_fields)

# # Custom User Model
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = [
#         ("super_admin", "Super Admin"),
#         ("author", "Author"),
#         ("user", "User"),
#     ]

#     email = models.EmailField(unique=True, blank=True, null=True)
#     phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)  # Needed for admin panel access
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

#     objects = CustomUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email if self.email else self.phone_number

#     # Permissions based on role
#     def has_blog_edit_permission(self):
#         """Allow only authors and super admins to create, edit, or delete blogs."""
#         return self.role in ["author", "super_admin"]

#     def has_comment_permission(self):
#         """All users can comment or read blogs."""
#         return self.role in ["user", "author", "super_admin"]

# # Author-specific Profile (optional, can be expanded as needed)
# class AuthorProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="author_profile")
#     bio = models.TextField(blank=True, null=True)
#     profile_picture = models.ImageField(upload_to="author_profiles", blank=True, null=True)

#     def __str__(self):
#         return f"Author Profile for {self.user.email or self.user.phone_number}"

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role="user", **extra_fields):
        """
        Creates and saves a User with either an email or a phone number.
        """
        if not username:
            raise ValueError("The Email or Phone number field is required")

        if "@" in username:
            extra_fields["email"] = self.normalize_email(username)
            extra_fields["phone_number"] = None
        else:
            extra_fields["phone_number"] = username
            extra_fields["email"] = None

        extra_fields["role"] = role

        # Ensure authors have staff access
        if role == "author":
            extra_fields["is_staff"] = True
        else:
            extra_fields["is_staff"] = False  # Ensure normal users don't get staff permissions

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)


        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with all permissions.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "super_admin")

        if not email:
            raise ValueError("Superuser must have an email")

        user = self.create_user(username=email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)  # Ensure the user is saved properly
        return user


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("super_admin", "Super Admin"),
        ("author", "Author"),
        ("user", "User"),
    ]

    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Needed for admin panel access
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]  # Allow login via phone number

    def __str__(self):
        return self.email if self.email else self.phone_number
    

    def has_blog_edit_permission(self):
        """Allow only authors and super admins to edit posts."""
        return self.role == "author" or self.is_superuser

    def has_comment_permission(self):
        """All users can comment or read blogs."""
        return self.role in ["user", "author", "super_admin"]
    
class AuthorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="author_profile")
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="author_profiles", blank=True, null=True)
    email=models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Author Profile for {self.user.email or self.user.phone_number}"
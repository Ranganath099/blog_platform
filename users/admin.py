from django.contrib import admin

# Register your models here.
from.models import CustomUser,AuthorProfile
admin.site.register(CustomUser)
admin.site.register(AuthorProfile)

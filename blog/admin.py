from django.contrib import admin
from .models import Category, Post, EmailVerification

# Register your models here.

# admin.site.register(Category)
# admin.site.register(Post)


# Menyra sesi duhet ta bejme admin paneling sepse na mundeson shtimin e filtrave, prepopulated fields etj.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author_name", "author", "is_published", "created_at")
    list_filter = ("category", "is_published", "created_at")
    search_fields = ("title", "content", "author_name")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")
    search_fields = ("user_username", "user_email", "token")
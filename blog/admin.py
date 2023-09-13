from django.contrib import admin
from blog.models import Blog, User, Comment, Like

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "password"

    )


admin.site.register(User, UserAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "author",
        
    )


admin.site.register(Blog, BlogAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blog",
        "content",
        "user",
        
    )


admin.site.register(Comment, CommentAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blog",
        "user",
    )


admin.site.register(Like, LikeAdmin)

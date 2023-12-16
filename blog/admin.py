from django.contrib import admin
from .models import Category, Post, Comment
from mptt.admin import DraggableMPTTAdmin
# Register your models here.

class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {'slug': ['name']}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'category', 'publish', 'status']
    list_filter = ['category', 'status']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
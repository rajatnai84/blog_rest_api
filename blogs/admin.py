from django.contrib import admin

from .models import Blog, Category, Comment, Tag

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog)
admin.site.register(Comment)

from django.contrib import admin
from .models import Video, Comment, Category, Like

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'video', 'author', 'created')


admin.site.register(Video)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Like)


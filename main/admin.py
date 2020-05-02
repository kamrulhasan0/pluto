from django.contrib import admin
from .models import Topic, Post, Clap, Comment,UserFollows
# Register your models here.

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Clap)
admin.site.register(Comment)
admin.site.register(UserFollows)

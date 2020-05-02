from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Topic(models.Model):
    topic_title = models.TextField()
    slug = models.SlugField(unique = True, blank = True)

    def __str__(self):
        return self.topic_title
    def save(self, *args, **kwargs):
        self.slug = self.slug or (slugify(self.topic_title))
        super().save(*args, **kwargs)

class Post(models.Model):
    title = models.TextField()
    intro = models.TextField(blank = True)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    slug = models.SlugField(unique = True, blank = True)
    num_claps = models.BigIntegerField(default = 0)
    num_comments = models.BigIntegerField(default = 0)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)



    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = self.slug or (slugify(self.title) + slugify(self.topic.topic_title) +slugify(str(self.date)))
        c_intro = ''
        for c in range(0,len(self.content)):
            c_intro += self.content[c]
            if(c == 20):
                break
        self.intro = self.intro or c_intro
        super().save(*args,**kwargs)


class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    follows = models.ForeignKey(Topic, on_delete = models.CASCADE)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    slug = models.SlugField(unique = True, blank = True)
    def save(self, *args, **kwargs):
        self.slug = self.slug or (slugify(self.comment_by.username) + slugify(self.post.title) +slugify(str(self.date)))
        super().save(*args,**kwargs)



class Clap(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    clappeded_by = models.ForeignKey(User, on_delete = models.CASCADE)

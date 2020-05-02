from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Topic, Post, Comment, UserFollows,Clap
from .forms import PostCreationForm,PostUpdateForm,CommentCreationForm

@login_required
def home(request):
    topics = request.user.userfollows_set.all()
    following_topics = True
    if(len(topics) == 0):
        following_topics = False
    posts = []
    for topic in topics:
        t_posts = topic.follows.post_set.all().order_by('-date')
        for t in t_posts:
            posts.append(t)
            print(t.date)
    context = {
    'following_topics':following_topics,
    'posts':posts
    }
    return render(request, 'main/home.html', context)

@login_required
def profile(request):
    posts = request.user.post_set.all().order_by('-date')
    post_exists = True
    if (len(posts) == 0):
        post_exists = False
    context = {
    'posts':posts,
    'post_exists':post_exists
    }
    return render(request, 'main/profile.html', context)

@login_required
def show_topics(request):
    follow = request.user.userfollows_set.all()
    topics = []
    for f in follow:
        topics.append(f.follows)
    no_topics = False
    if (len(topics) == 0):
        no_topics = True
    context = {
    'topics':topics,
    'no_topics':no_topics
    }
    return render(request, 'main/show_topics.html', context)

@login_required
def discover_topics(request):
    topics =  Topic.objects.all()
    follow = request.user.userfollows_set.all()
    f_topics = []
    d_topics = []
    for f in follow:
        f_topics.append(f.follows)
    print(f_topics)
    print(d_topics)
    for topic in topics:
        if topic not in f_topics:
            d_topics.append(topic)
    no_topic_left = False
    if(len(d_topics) == 0):
        no_topic_left = True
    context = {
    'topics':d_topics,
    'no_topic_left':no_topic_left
    }
    return render(request, 'main/discover_topics.html', context)


@login_required
def show_topic_posts(request, slug):
    topic = get_object_or_404(Topic, slug = slug)
    posts = topic.post_set.all().order_by('-num_claps')
    context = {
    'topic':topic,
    'posts':posts
    }
    return render(request, 'main/show_topic_posts.html', context)

@login_required
def follow_topic(request, slug):
    topic = get_object_or_404(Topic, slug = slug)
    following_topics = request.user.userfollows_set.filter(follows = topic)
    if(len(following_topics) != 0):
        messages.warning(request, "You are already following this topic")
        return redirect('main:show_topic_posts', slug)
    UserFollows.objects.create(user = request.user, follows = topic)
    messages.success(request, "You have followed this topic!")
    return redirect('main:show_topic_posts', slug)

@login_required
def unfollow_topic(request, slug):
    topic = get_object_or_404(Topic, slug = slug)
    request.user.userfollows_set.filter(follows = topic).delete()
    messages.success(request, "You unfollwed this topic!")
    return redirect('main:show_topic_posts', slug)


@login_required
def create_post(request, slug):
    topic = get_object_or_404(Topic, slug = slug)
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.topic = topic
            form.save()
            messages.success(request, 'Post was created successfully!')
            return redirect('main:home')
    else:
        form = PostCreationForm()
    context = {'form':form}
    return render(request, 'main/create_post.html', context)


@login_required
def update_post(request,slug):
    post = get_object_or_404(Post, slug = slug)
    if post.author != request.user :
        return HttpResponse(status = 403)
    if request.method == "POST":
        form = PostUpdateForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            messages.success(request, 'Post has been Updated')
            return redirect('main:view_post', post.slug)
    else:
        form = PostUpdateForm(instance = post)
    context = {'form':form}
    return render(request, 'main/update_post.html', context)


@login_required
def view_post(request, slug):
    post = get_object_or_404(Post, slug = slug)
    claps = post.clap_set.filter(clappeded_by = request.user)
    if(len(claps) != 0):
        clapped = True
    else:
        clapped = False
    context = {
    'post':post,
    'clapped':clapped
    }
    return render(request, 'main/view_post.html', context)



@login_required
def delete_post_confirmation(request, slug):
    post = get_object_or_404(Post, slug = slug)
    if post.author != request.user:
        return HttpResponse(status = 403)
    context = {
    'post': post,
    'slug':slug
    }
    return render(request, 'main/delete_post_confirmation.html', context)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug = slug)
    if post.author != request.user:
        return HttpResponse(status = 403)
    post.delete()
    messages.success(request, 'Post was deleted successfully!')
    return redirect('main:home')

@login_required
def comment(request, slug):
    post = get_object_or_404(Post, slug = slug)
    if(request.method == "POST"):
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            form.instance.post = post
            form.instance.comment_by = request.user
            form.save()
            post.num_comments += 1
            post.save()
            messages.success(request, 'Response added successfully!')
            return redirect('main:show_comments', post.slug)
    else:
        form = CommentCreationForm()
    context = {
    'form':form,
    'post':post
    }
    return render(request, 'main/comment.html', context)

@login_required
def show_comments(request, slug):
    post = get_object_or_404(Post, slug = slug)
    comments = post.comment_set.all()
    no_comments = True
    if len(comments) != 0:
        no_comments = False
    context ={
    'comments':comments,
    'no_comments':no_comments,
    'post':post
    }
    return render(request, 'main/show_comments.html', context)

@login_required
def clap(request, slug):
    post = get_object_or_404(Post, slug = slug)
    claps = post.clap_set.filter(clappeded_by = request.user)
    if(len(claps) != 0 ):
        return redirect('main:view_post', slug)
    else:
        Clap.objects.create(post = post, clappeded_by = request.user)
        post.num_claps += 1
        post.save()
        messages.success(request, 'Clap Added!!!')
        return redirect('main:view_post', slug)

@login_required
def un_clap(request, slug):
    post = get_object_or_404(Post, slug = slug)
    claps = post.clap_set.filter(clappeded_by = request.user)
    if(len(claps) == 0):
        return redirect('main:view_post', slug)
    else:
        post.clap_set.filter(clappeded_by = request.user).delete()
        post.num_claps -= 1
        post.save()
        messages.success(request, 'Clap Removed')
        return redirect('main:view_post', slug)

@login_required
def delete_comment(request, slug1, slug2):
    comment = request.user.comment_set.filter(slug = slug1)
    if(len(comment) == 0):
        return HttpResponse(status = 404)
    post = comment[0].post
    comment[0].delete()
    post.num_comments -= 1
    post.save()
    messages.success(request, "Response Removed!!!")
    return redirect('main:show_comments', slug2)
@login_required
def about(request):
    return render(request, 'main/about.html')

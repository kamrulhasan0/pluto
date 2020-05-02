from django.urls import path
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profile/', views.profile, name = 'profile'),
    path('show-topics/', views.show_topics, name = 'show_topics'),
    path('discover-topics/', views.discover_topics, name = 'discover_topics'),
    path('follow-topic/<slug:slug>/', views.follow_topic, name = 'follow_topic'),
    path('unfollow-topic/<slug:slug>/', views.unfollow_topic, name = 'unfollow_topic'),
    path('show-topic-posts/<slug:slug>/', views.show_topic_posts, name = 'show_topic_posts'),
    path('create-post/<slug:slug>/', views.create_post, name = 'create_post'),
    path('update-post/<slug:slug>/', views.update_post, name = 'update_post'),
    path('view-post/<slug:slug>/', views.view_post, name = 'view_post'),
    path('delete-post-confirmation/<slug:slug>/', views.delete_post_confirmation, name = 'delete_post_confirmation'),
    path('delete-post/<slug:slug>/', views.delete_post, name = 'delete_post'),
    path('comment/<slug:slug>/', views.comment, name = 'comment'),
    path('show-comments/<slug:slug>/', views.show_comments, name = 'show_comments'),
    path('clap/<slug:slug>/', views.clap, name = 'clap'),
    path('unclap/<slug:slug>/', views.un_clap, name = 'un_clap'),
    path('delete-comment/<slug:slug1>/<slug:slug2>/', views.delete_comment, name = 'delete_comment'),
    path('about/', views.about, name = 'about'),

]

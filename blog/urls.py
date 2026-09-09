from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('health/', views.health, name='health'),

    path('posts/', views.post_list, name='post_list'),
    path('posts/my-posts/', views.my_posts, name='my_posts'),
    path('posts/create/', views.create_post, name='create_post'),

    path('register/', views.register_view, name='register'),
    path('verification-sent/', views.verification_sent, name='verification_sent'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

    path('posts/<slug:slug>/', views.post_details, name='post_detail'),
    path('posts/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('posts/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('posts/<slug:slug>/like/', views.like_post, name='like_post'),
]
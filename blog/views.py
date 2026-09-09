import uuid
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import RegisterForm, PostForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, EmailVerification
from django.http import HttpResponse

def health(request):
    return HttpResponse("OK")

def home(request):
    return render(request, 'blog/home.html')

def post_list(request):
    posts = Post.objects.filter(is_published = True).order_by('-created_at')
    categories = Category.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        posts = posts.filter(title__icontains=query)

    if category_id:
        posts = posts.filter(category_id=category_id)

    context = {
        'posts': posts,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    }

    return render(request, 'blog/post_list.html', context)

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    user_liked = False

    if request.user.is_authenticated:
        user_liked = post.likes.filter(id=request.user.id).exists()

    context = {
        'post': post,
        'user_liked': user_liked
    }
    return render(request, "blog/post_details.html", context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_name = request.user.username
            post.save()
            return redirect('post_detail', slug = post.slug)
        
    else:
        form = PostForm()

    context = {
        'form': form,
        'title': 'Create Post',
        'button_text': 'Create'
    }

    return render(request, 'blog/post_form.html', context)

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return redirect('post_detail', slug = post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('post_detail', slug = post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'title': 'Edit Post',
        'button_text': 'Update'
    }

    return render(request, 'blog/post_form.html', context)

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return redirect('post_detail', slug = post.slug)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author = request.user).order_by('-created_at')

    context = {
        'posts': posts
    }
    return render(request, 'blog/my_posts.html', context)

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug) 

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', slug = post.slug)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = str(uuid.uuid4())

            EmailVerification.objects.create(
                user=user,
                token = token
            )

            verification_url = request.build_absolute_uri(reverse('verify_email', args=[token]))
            send_mail(subject='Verify your DTI Blog Account', 
                      message=f'Click this link to verify your account (valid only for 5 minutes): {verification_url}',
                      from_email=None,
                      recipient_list=[user.email],
                      fail_silently=False
                      )
            return redirect('verification_sent')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})

def verification_sent(request):
    return render(request, 'blog/verification_sent.html')


def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token = token)

    if verification.is_expired():
        return render(request, 'blog/verification_failed.html')
    
    user = verification.user
    user.is_active = True
    user.save()

    verification.delete()

    return render(request, 'blog/verification_success.html')




def about(request):
    return render(request, 'blog/about.html')


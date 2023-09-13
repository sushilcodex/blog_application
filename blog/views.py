from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment, Like
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from blog.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse


@login_required 
def blog_list(request):
    try:
        if hasattr(request, 'filtered_blogs'):
            blogs = request.filtered_blogs
        else:
            blogs = Blog.objects.all().order_by('-id')

        page = request.GET.get('page1', 1)
        paginator = Paginator(blogs, 5)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog_list.html', {'blogs': blogs})


@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    likes = Like.objects.filter(blog=blog)
    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments, 'likes': likes})

@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(blog=blog, user=request.user, content=content)
        messages.add_message(request, messages.INFO, "Comment added to blog.")
    return redirect('blog:blog_detail', blog_id=blog_id)

@login_required
def add_like(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    Like.objects.create(blog=blog, user=request.user)
    messages.add_message(request, messages.INFO, "Like added to blog.")
    return redirect('blog:blog_detail', blog_id=blog_id)


def signup(request):
    
    if request.method == 'POST':
        User.objects.create(
            username=request.POST.get('email'),
            email=request.POST.get('email'),
            password=make_password(request.POST.get('pswd')),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
        )
        return redirect('blog:login')
    else:
        return render(request, 'registration/signup.html')


def user_login(request):

    if request.method == 'POST':
        user=authenticate(username=request.POST.get('email'),password=request.POST.get('pswd'))
        if user:
           login(request, user)
           return redirect('blog:blog_list')
        else:
            messages.add_message(request, messages.INFO, "Invalid credentials.")
            return redirect('blog:login')
    
    else:
        return render(request, 'registration/login.html')


@login_required
def blog_email(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        recipient_list = request.POST.get('email')
        context = {
            "request": request,
            "content": blog.content,
        }
        body_text_content = render_to_string("blog/blog_email.html")
        subject = "Blog"
        html_content = render_to_string("blog/blog_email.html", context)

        try:
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=body_text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient_list],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()
        except Exception as e:
            messages.add_message(request, messages.INFO, "There is an error while sending email.")
            return redirect('blog:blog_detail',blog_id=blog_id)
        messages.add_message(request, messages.INFO, "Email has been sent successfuly.")
        return redirect('blog:blog_detail',blog_id=blog_id)

    return render(request, 'blog/email.html', {'blog': blog})


def logout_user(request):
    logout(request)
    return redirect(reverse('blog:login'))
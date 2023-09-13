# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog-listing', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('blog/<int:blog_id>/like/', views.add_like, name='add_like'),
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('blog/<int:blog_id>/email/', views.blog_email, name='blog_email'),
    path('logout/', views.logout_user, name='logout'),

]

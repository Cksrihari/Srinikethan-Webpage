from django.urls import path
from . import views

urlpatterns = [
    path('account/two_factor/update/', views.UpdateTwoFactorView.as_view(), name='two_factor_update'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('insights/', views.insights, name='insights'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('account/post-login/', views.post_login_redirect, name='post_login_redirect'),
]
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.profiles_list, name='profiles_list'),
    re_path(r'^profiles/(?P<key>[A-Za-z0-9\-\_]+)/$', views.profile_detail, name='profile_detail'),
    path('news/', views.news_redirect, name='news_redirect'),
    path('news/list/', views.news_list, name='news_list'),
]

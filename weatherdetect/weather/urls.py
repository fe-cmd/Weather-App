from unicodedata import name
from django.urls import path
from .import views
urlpatterns = [
    path('welcome', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('intro', views.intro, name='intro'),
    path('logout', views.logout, name='logout')
]

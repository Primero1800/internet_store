from django.urls import path

from posts.views import index, information

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('information/', information, name='information'),
]
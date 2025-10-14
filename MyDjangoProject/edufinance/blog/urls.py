from django.urls import path
from .views import home, post_list

urlpatterns = [
    path('', home, name='home'),
    path('posts', post_list, name='posts')
]

from django.urls import path
from .views import home, post_form, post_list, post_detail

urlpatterns = [
    path('', home, name='home'),
    path('posts', post_list, name='posts'),
    path('post-form', post_form, name='post_form'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
]

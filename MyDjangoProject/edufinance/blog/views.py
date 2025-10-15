from turtle import title
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post


# # Create your views here.
# def home(request):
    
#     return HttpResponse("Hello World")


def home(request):

    return render(request, 'pages/home.html',  {'name': 'James'})

def post_list(request):
    posts = Post.objects.all()

    return render(request, 'pages/posts.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk)
    return render(request, 'pages/post_details', {'post': post})
from turtle import title
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse

from .forms import PostForm
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
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pages/post_details.html', {'post': post})


def post_form(request):
    form = PostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'pages/post_form.html', {'form': form})


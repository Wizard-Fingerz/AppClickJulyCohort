from turtle import title
from django.shortcuts import render
from django.http import HttpResponse



# # Create your views here.
# def home(request):
    
#     return HttpResponse("Hello World")


def home(request):

    return render(request, 'pages/home.html',  {'name': 'James'})

def post_list(request):
    posts = [
        {'title': 'Presidential Election in Nigeria', 'body': "There is an alarming rate of corruption during the presidential election in Nigeria"},
        {'title': 'Organised Crimes around Lagos', 'body': 'It was recorded that over the decades, we have at least 50 victims of organised crimes per year in Lagos state'},
        {'title': 'Presidential Election in Nigeria', 'body': "There is an alarming rate of corruption during the presidential election in Nigeria"},
        {'title': 'Organised Crimes around Lagos', 'body': 'It was recorded that over the decades, we have at least 50 victims of organised crimes per year in Lagos state'},
        {'title': 'Presidential Election in Nigeria', 'body': "There is an alarming rate of corruption during the presidential election in Nigeria"},
        {'title': 'Organised Crimes around Lagos', 'body': 'It was recorded that over the decades, we have at least 50 victims of organised crimes per year in Lagos state'},
        {'title': 'Hackaton Projects in Appclick Academy', 'body': 'We have two week starting from next week to carry out our hackaton project'},
    ]

    return render(request, 'pages/posts.html', {'posts': posts})
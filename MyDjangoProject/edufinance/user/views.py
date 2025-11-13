from django.shortcuts import render
from django.views import View
from django.http import HttpResponse



# Create your views here.

class UserView(View):

    def get(self, request):
        return HttpResponse("Hello from Class Based View in User")

def login(request):
    return render(request, 'pages/login.html')
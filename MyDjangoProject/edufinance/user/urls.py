from django.urls import path
from .views import UserView, login

urlpatterns = [
    path('user/', UserView.as_view()),
    path('login/', login, name='login'),
]

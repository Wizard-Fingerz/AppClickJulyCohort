
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.authtoken import views
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='obtain_auth_token'),
]

# Include both the router URLs and the token auth endpoint
urlpatterns += router.urls

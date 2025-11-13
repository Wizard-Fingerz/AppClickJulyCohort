
from rest_framework.routers import DefaultRouter
from .classroom.views import ClassroomViewSet
from .course.views import CourseViewSet

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = router.urls
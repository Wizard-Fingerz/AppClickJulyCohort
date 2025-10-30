from rest_framework import viewsets
from .models import Classroom
from .serializers import ClassroomSerializers

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializers
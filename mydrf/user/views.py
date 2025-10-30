from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        student = self.get_object()
        return Response({'name': student.name, 'course': student.course})

    @action(detail=False, methods=['get'])
    def top_students(self, request):
        top_students = Student.objects.filter(age__gt=20)
        serializer = self.get_serializer(top_students, many=True)
        return Response(serializer.data)
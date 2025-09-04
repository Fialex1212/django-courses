from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

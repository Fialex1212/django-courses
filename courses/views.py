from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, status
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from users.models import UserCourseAccess
from django.db.models import Q


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.filter(is_free=True)

        accessible_course_ids = UserCourseAccess.objects.filter(user=user).values_list(
            "course_id", flat=True
        )

        return Lesson.objects.filter(
            Q(is_free=True) | Q(course_id__in=accessible_course_ids)
        )



class UploadLessonVideo(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        file_obj = request.data["video"]
        lesson.video.save(file_obj.name, file_obj, save=True)
        return Response({"message": "Відео завантажено"})

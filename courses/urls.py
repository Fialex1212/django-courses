from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, UploadLessonVideo

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("upload-video/<int:lesson_id>/", UploadLessonVideo.as_view(), name="upload-video"),
]

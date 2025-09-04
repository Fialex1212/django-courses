from .models import Course, Lesson
from rest_framework import serializers
from drf_extra_fields.fields import FileField
from django.core.files.storage import default_storage
from drf_spectacular.utils import extend_schema_field, OpenApiTypes


class LessonSerializer(serializers.ModelSerializer):
    video = FileField(
        required=True,
        write_only=True,
        help_text="Upload file",
    )
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "description",
            "position",
            "is_published",
            "duration_seconds",
            "created_at",
            "updated_at",
            "video",
            "video_url",
        ]
        read_only_fields = [
            "id",
            "video",
            "video_url",
            "created_at",
            "updated_at",
        ]
    
    @extend_schema_field(OpenApiTypes.BINARY)
    def get_preview(self, obj):
        return obj.preview

    def create(self, validated_data):
        video = validated_data.pop("video", None)
        lesson = super().create(validated_data)
        if video:
            from django.core.files.storage import default_storage

            path = default_storage.save(f"lessons/videos/{video.name}", video)
            lesson.video = path
            lesson.save()
        return lesson
    
    
    @extend_schema_field(OpenApiTypes.BINARY)
    def get_video(self, obj):
        return obj.video

    @extend_schema_field(OpenApiTypes.URI)
    def get_video_url(self, obj):
        if not obj.video:
            return None
        request = self.context.get("request")
        url = default_storage.url(obj.video.name)
        if request:
            return request.build_absolute_uri(url)
        return url


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    preview = FileField(
        required=True,
        write_only=True,
        help_text="Upload file",
    )
    preview_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "preview",
            "preview_url",
            "created_at",
            "updated_at",
            "lessons",
        ]

    @extend_schema_field(OpenApiTypes.BINARY)
    def get_preview(self, obj):
        return obj.preview

    @extend_schema_field(OpenApiTypes.URI)
    def get_preview_url(self, obj):
        request = self.context.get("request")
        if obj.preview and request:
            return request.build_absolute_uri(obj.preview.url)
        return None

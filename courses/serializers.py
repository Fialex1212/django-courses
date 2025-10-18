from .models import Course, Lesson, HomeWork
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = [
            "id",
            "lesson",
            "title",
            "description",
            "link",
            "created_at",
            "updated_at",
            "duration_seconds",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.FileField(
        required=True,
        write_only=True,
        help_text="Upload video file",
    )
    video_url = serializers.SerializerMethodField(read_only=True)
    homework = HomeWorkSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "description",
            "position",
            "is_free",
            "duration_seconds",
            "created_at",
            "updated_at",
            "video",
            "video_url",
            "homework"
        ]
        read_only_fields = [
            "id",
            "video_url",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.BINARY)
    def get_preview(self, obj):
        return obj.preview

    def create(self, validated_data):
        return super().create(validated_data)

    @extend_schema_field(OpenApiTypes.BINARY)
    def get_video(self, obj):
        return obj.video

    @extend_schema_field(OpenApiTypes.URI)
    def get_video_url(self, obj):
        if not obj.video:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    preview = serializers.ImageField(
        required=True,
        write_only=True,
        help_text="Upload preview image",
    )
    preview_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "subtitle",
            "price",
            "discount_price",
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
        if not obj.preview:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.preview.url)
        return obj.preview.url

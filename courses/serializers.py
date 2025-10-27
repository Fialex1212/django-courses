from courses.models import Course, Lesson, HomeWork
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from users.models import UserCourseAccess


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
            "homework",
        ]
        read_only_fields = [
            "id",
            "video_url",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.URI)
    def get_video_url(self, obj):
        request = self.context.get("request")
        if not obj.video:
            return None
        if request:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        user = request.user if request else None

        has_access = instance.is_free or (
            user
            and user.is_authenticated
            and UserCourseAccess.objects.filter(
                user=user, course=instance.course
            ).exists()
        )

        if not has_access:
            data["video_url"] = None
            data["video_locked"] = True
        else:
            data["video_locked"] = False

        return data


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    preview = serializers.ImageField(
        required=True,
        write_only=True,
        help_text="Upload preview image",
    )
    preview_url = serializers.SerializerMethodField(read_only=True)
    preview_video = serializers.SerializerMethodField(read_only=True)

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
            "preview_video",
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

    @extend_schema_field(OpenApiTypes.URI)
    def get_preview_video(self, obj):
        if not obj.video:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url

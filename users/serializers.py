from rest_framework import serializers
from users.models import User, UserCourseAccess
from courses.models import Course


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "telegram", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            telegram=validated_data["telegram"],
            password=validated_data["password"],
        )
        return user


class CourseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title"]


class UserCourseAccessSerializer(serializers.ModelSerializer):
    course = CourseShortSerializer(read_only=True)

    class Meta:
        model = UserCourseAccess
        fields = ["course", "activated_at"]


class UserSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "telegram",
            "email",
            "courses",
        ]

    def get_courses(self, obj):
        accesses = obj.course_accesses.select_related("course")
        return [
            {
                "id": access.course.id,
                "title": access.course.title,
            }
            for access in accesses
        ]

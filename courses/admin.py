from django.db import models
from django.contrib import admin
from .models import Course, Lesson, HomeWork


class HomeWorkInline(admin.TabularInline):
    model = HomeWork
    extra = 0
    fields = ("title", "description", "link")
    readonly_fields = ()


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = (
        "position",
        "title",
        "description",
        "is_free",
        "video",
    )
    readonly_fields = ()
    ordering = ("position",)
    show_change_link = True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "position",
        "is_free",
        "video",
        "duration_seconds",
    )
    list_filter = ("course", "is_free")
    search_fields = ("title", "description")
    ordering = ("course", "position")
    fields = (
        "course",
        "title",
        "description",
        "position",
        "is_free",
        "video",
        "duration_seconds",
    )
    inlines = [HomeWorkInline]

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        course_id = request.GET.get("course")
        if course_id:
            last_position = (
                Lesson.objects.filter(course_id=course_id).aggregate(
                    models.Max("position")
                )["position__max"]
                or 0
            )
            initial["position"] = last_position + 1
        return initial


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at", "updated_at", "preview")
    list_filter = ("created_at",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "description",
        "link",
        "created_at",
        "updated_at",
    )
    list_filter = ("lesson", "created_at")
    search_fields = ("title", "description", "link")

from django.db import models
from django.contrib import admin
from .models import Course, Lesson
from django.core.files.storage import default_storage


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = (
        "position",
        "title",
        "description",
        "is_published",
        "video",
    )
    readonly_fields = ()
    ordering = ("position",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position", "is_published", "video")
    list_filter = ("course", "is_published")
    ordering = ("course", "position")
    fields = ("course", "title", "description", "position", "is_published", "video")

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        course_id = request.GET.get("course")
        if course_id:
            last_position = Lesson.objects.filter(course_id=course_id).aggregate(models.Max('position'))['position__max']
            initial['position'] = (last_position or 0) + 1
        return initial


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at", "updated_at", "preview",)
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


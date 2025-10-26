from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from courses.models import Lesson
from .models import User, UserCourseAccess, UserLessonAccess
from django.core.exceptions import ValidationError


# --- Inline для уроков ---
class UserLessonAccessInline(admin.TabularInline):
    model = UserLessonAccess
    extra = 0
    fields = ("lesson",)
    readonly_fields = ()

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            completed_lessons_ids = UserLessonAccess.objects.filter(
                user=obj
            ).values_list("lesson_id", flat=True)
            formset.form.base_fields["lesson"].queryset = Lesson.objects.exclude(
                id__in=completed_lessons_ids
            )
        return formset


# --- Inline для курсов ---
class UserCourseAccessInline(admin.TabularInline):
    model = UserCourseAccess
    extra = 0
    fields = ("course", "activated_at")
    readonly_fields = ("activated_at",)


# --- Админка пользователя ---
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    inlines = [UserCourseAccessInline, UserLessonAccessInline]

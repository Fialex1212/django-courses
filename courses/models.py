from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Course Title")
    subtitle = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Course Subtitle"
    )
    video = models.FileField(
        upload_to="courses/videos/",
        blank=True,
        null=True,
        verbose_name="Video file",
    )
    price = models.IntegerField(blank=True, null=True, verbose_name="Price")
    discount_price = models.IntegerField(
        blank=True, null=True, verbose_name="Discounted price"
    )
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    preview = models.FileField(
        upload_to="courses/previews/",
        blank=True,
        null=True,
        verbose_name="Preview Image",
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.CASCADE, db_index=True
    )
    title = models.CharField(max_length=255, verbose_name="Lesson Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    duration = models.IntegerField(
        null=True, blank=True, default=0, verbose_name="Duration"
    )
    position = models.PositiveIntegerField(
        default=1, db_index=True, verbose_name="Position"
    )

    video = models.FileField(
        upload_to="lessons/videos/",
        blank=True,
        null=True,
        verbose_name="Video file",
    )

    is_free = models.BooleanField(default=False, verbose_name="Is Free")
    duration_seconds = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Duration (seconds)"
    )

    class Meta:
        ordering = ["course", "position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "position"],
                name="unique_lesson_position_per_course",
            )
        ]

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class HomeWork(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="homework", on_delete=models.CASCADE, db_index=True
    )
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    link = models.TextField(blank=True, null=True, verbose_name="Link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

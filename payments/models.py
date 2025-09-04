from django.db import models
from django.conf import settings
from courses.models import Course


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="User",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Course",
    )
    provider = models.CharField(max_length=50, verbose_name="Payment provider")
    status = models.CharField(max_length=20, default="pending", verbose_name="Status")
    transaction_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Transaction ID"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} – {self.course} – {self.provider} ({self.status})"

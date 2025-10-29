from django.db import models
from django.conf import settings
from courses.models import Course


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Очікує оплати"),
        ("paid", "Оплачено"),
        ("canceled", "Скасовано"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    invoice = models.FileField(
        upload_to="orders/invoices/",
        blank=True,
        null=True,
        verbose_name="Invoice file",
    )

    def __str__(self):
        return f"Замовлення {self.id} — {self.user.email} — {self.status}"

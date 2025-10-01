from django.db import models
from django.conf import settings
from courses.models import Course

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("canceled", "Отменён"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} — {self.user.email} — {self.status}"

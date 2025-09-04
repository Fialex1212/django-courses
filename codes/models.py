from django.db import models
from courses.models import Course
from users.models import User

# Create your models here.
class ActivationCode(models.Model):
    code = models.CharField(max_length=12, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchased_codes')
    activated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activated_codes')
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def is_used(self):
        return self.activated_by is not None
    is_used.boolean = True
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .services import confirm_order


@receiver(post_save, sender=Order)
def order_paid_handler(sender, instance, **kwargs):
    if instance.status == "paid":
        if not instance.user.purchased_codes.filter(course=instance.course).exists():
            confirm_order(instance)

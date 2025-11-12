from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tasks import confirm_order_task

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    if not created and old_status != "paid" and instance.status == "paid":
        confirm_order_task.delay(order_id=instance.id)

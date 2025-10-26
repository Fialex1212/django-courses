from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
from .services import confirm_order


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_status = Order.objects.get(pk=instance.pk).status
        except Order.DoesNotExist:
            instance._old_status = None


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    if not created and old_status != "paid" and instance.status == "paid":
        confirm_order(
            instance
        )

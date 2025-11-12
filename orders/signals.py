from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
from .tasks import confirm_order_task

# 1️⃣ Сохраняем старый статус до сохранения заказа
@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Order.objects.get(pk=instance.pk)
        instance._old_status = old_instance.status

# 2️⃣ После сохранения проверяем, изменился ли статус на "paid"
@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    # если заказ не новый, и статус изменился на "paid"
    if not created and old_status != "paid" and instance.status == "paid":
        # вызываем Celery таску, которая создаст код и отправит письмо
        confirm_order_task.delay(order_id=instance.id)

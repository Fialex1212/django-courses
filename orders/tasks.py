from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from codes.models import ActivationCode
from codes.utils import generate_activation_code
from orders.models import Order
from codes.models import ActivationCode


@shared_task
def confirm_order_task(order_id):

    order = Order.objects.get(id=order_id)

    code = ActivationCode.objects.create(
        code=generate_activation_code(),
        course=order.course,
        purchased_by=order.user,
        price_paid=order.amount,
    )

    send_mail(
        subject="Ваш код активації",
        message=f"Дякуємо за покупку курсу {order.course.title}!\n\nКод активації: {code.code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
    )

    return code.code

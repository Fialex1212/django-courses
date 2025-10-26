from django.core.mail import send_mail
from django.conf import settings
from codes.models import ActivationCode
from codes.utils import generate_activation_code


def confirm_order(order):
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

    return code

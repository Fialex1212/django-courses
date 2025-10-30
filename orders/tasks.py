from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from codes.models import ActivationCode
from codes.utils import generate_activation_code

@shared_task
def confirm_order_task(order_id, course_title, user_email, amount):
    code = ActivationCode.objects.create(
        code=generate_activation_code(),
        course_id=order_id,
        purchased_by_id=order_id,
        price_paid=amount,
    )

    send_mail(
        subject="Ваш код активації",
        message=f"Дякуємо за покупку курсу {course_title}!\n\nКод активації: {code.code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )

    return code.code

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_card_payment_intent(course, user):
    intent = stripe.PaymentIntent.create(
        amount=int(course.price * 100),
        currency="uah",
        payment_method_types=["card"],
        metadata={
            "course_id": str(course.id),
            "user_id": str(user.id),
        },
    )
    return intent

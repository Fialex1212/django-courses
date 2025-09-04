from .stripe import create_card_payment_intent
from rest_framework.decorators import api_view
from rest_framework.response import Response
from courses.models import Course
from .models import Payment
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import stripe


@api_view(["POST"])
def start_stripe_payment(request):
    course_id = request.data.get("course_id")
    user = request.user

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    intent = create_card_payment_intent(course, user)
    return Response(
        {
            "type": "card",
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
        }
    )


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]

        course_id = intent["metadata"].get("course_id")
        user_id = intent["metadata"].get("user_id")

        if not course_id or not user_id:
            return HttpResponse(status=400)

        User = get_user_model()

        try:
            course = Course.objects.get(id=course_id)
            user = User.objects.get(id=user_id)
        except (Course.DoesNotExist, User.DoesNotExist):
            return HttpResponse(status=404)

        Payment.objects.create(
            user=user,
            course=course,
            provider="stripe",
            status="success",
            transaction_id=intent["id"],
        )

    return HttpResponse(status=200)

from django.urls import path
from . import views

urlpatterns = [
    path("stripe/start/", views.start_stripe_payment),
    path("stripe/webhook/", views.stripe_webhook),
]

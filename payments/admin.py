from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
        "provider",
        "status",
        "transaction_id",
        "created_at",
    )
    list_filter = ("provider", "status", "created_at")
    search_fields = ("user__username", "user__email", "course__title", "transaction_id")
    readonly_fields = ("created_at", "transaction_id")
    ordering = ("-created_at",)
    list_select_related = ("user", "course")

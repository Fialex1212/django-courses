from django.contrib import admin
from .models import ActivationCode


@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "course",
        "purchased_by",
        "activated_by",
        "price_paid",
        "created_at",
        "used_at",
        "is_used",
    )
    list_filter = ("course", "purchased_by", "activated_by")
    search_fields = ("code",)

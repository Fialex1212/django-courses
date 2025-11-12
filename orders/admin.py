from django.utils.html import format_html
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "amount", "status", "invoice", "created_at")
    list_filter = ("status", "course")

    @admin.register(Order)
    def colored_status(self, obj):
        if obj.status == "paid":
            color = "green"
        elif obj.status == "pending":
            color = "blue"
        elif obj.status == "canceled":
            color = "red"
        else:
            color = "black"
        return format_html(
            '<span style="color: {};"><strong>{}</strong></span>',
            color,
            obj.get_status_display(),
        )

    colored_status.short_description = "Status"
    actions = ["mark_as_paid"]

    def mark_as_paid(self, request, queryset):
        for order in queryset:
            order.status = "paid"
            order.save()
        self.message_user(request, "Вибрані замовлення позначено як оплачені")

    mark_as_paid.short_description = "Позначити як оплачені"

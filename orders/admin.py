from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "amount", "status", "created_at")
    list_filter = ("status", "course")
    actions = ["mark_as_paid"]

    def mark_as_paid(self, request, queryset):
        for order in queryset:
            order.status = "paid"
            order.save()
        self.message_user(request, "Выбранные заказы отмечены как оплаченные")

    mark_as_paid.short_description = "Отметить как оплаченные"

from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "course", "amount", "status", "invoice", "created_at"]
        read_only_fields = ["id", "user", "amount", "status", "invoice", "created_at"]

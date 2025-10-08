from rest_framework import serializers

class ActivateCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=12)

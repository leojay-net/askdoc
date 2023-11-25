from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    problem = serializers.CharField(max_length=300)
    symptoms = serializers.CharField(max_length=300)
    medical_history = serializers.CharField(max_length=300)
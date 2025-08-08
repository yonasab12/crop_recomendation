# api/serializers.py
from rest_framework import serializers

class PredictionInputSerializer(serializers.Serializer):
    N = serializers.FloatField()
    P = serializers.FloatField()
    K = serializers.FloatField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
    ph = serializers.FloatField()
    rainfall = serializers.FloatField()

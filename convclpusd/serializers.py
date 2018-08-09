from rest_framework import serializers

class ConversionSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=8)
    exact_date = serializers.BooleanField()
    date = serializers.DateField()


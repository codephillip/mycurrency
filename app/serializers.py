from django.utils import timezone
from rest_framework import serializers

from mycurrency.constants import DATE_FORMAT
from .services.currency_service import save_exchanges_async


class CurrencyRateParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField(input_formats=[DATE_FORMAT])
    date_to = serializers.DateField(input_formats=[DATE_FORMAT])
    source_currency = serializers.CharField(max_length=3)

    def validate(self, data):
        if data.get('date_from') >= data.get('date_to'):
            raise serializers.ValidationError("date_from must be before date_to")
        return data


class CurrencyConverterParamsSerializer(serializers.Serializer):
    source_currency = serializers.CharField(max_length=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    exchanged_currency = serializers.CharField(max_length=3)

    def validate(self, data):
        if data.get('source_currency') == data.get('exchanged_currency'):
            raise serializers.ValidationError("Source and exchanged currency must be different")
        return data


class TWRRParamsSerializer(serializers.Serializer):
    source_currency = serializers.CharField(max_length=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    exchanged_currency = serializers.CharField(max_length=3)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField(required=False)

    def validate(self, data):
        start_date = data.get('start_date').astimezone(timezone.utc) if data.get('start_date') else None

        if start_date and start_date > timezone.now():
            raise serializers.ValidationError({'start_date': 'Start date cannot be in the future'})
        if data.get('end_date') and data.get('end_date') <= start_date:
            raise serializers.ValidationError({'end_date': 'End date must be greater than start date'})
        return data


class CurrencyExchangeRateSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    timestamp = serializers.IntegerField()
    base = serializers.CharField(max_length=3)
    date = serializers.DateField()
    rates = serializers.DictField(child=serializers.DecimalField(max_digits=18, decimal_places=6))

    def create(self, validated_data):
        date = validated_data.pop('date')
        rates_data = validated_data.pop('rates')
        base_currency = validated_data.pop('base')
        save_exchanges_async(base_currency, date, rates_data)
        return validated_data

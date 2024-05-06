from rest_framework import serializers

from mycurrency.constants import DATE_FORMAT


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
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        if data.get('end_date') and data.get('end_date') <= data.get('start_date'):
            raise serializers.ValidationError({'end_date': 'End date must be greater than start date'})
        return data

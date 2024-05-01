from rest_framework import serializers


class CurrencyRateQueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField(input_formats=['%Y-%m-%d'])
    date_to = serializers.DateField(input_formats=['%Y-%m-%d'])
    source_currency = serializers.CharField(max_length=3)

    def validate(self, data):
        if data.get('date_from') >= data.get('date_to'):
            raise serializers.ValidationError("date_from must be before date_to")
        return data


class CurrencyConverterSerializer(serializers.Serializer):
    source_currency = serializers.CharField(max_length=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    exchanged_currency = serializers.CharField(max_length=3)

    def validate(self, data):
        if data.get('source_currency') == data.get('exchanged_currency'):
            raise serializers.ValidationError("Source and exchanged currency must be different")
        return data

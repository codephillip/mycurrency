from rest_framework import serializers


class CurrencyRateQueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField(input_formats=['%Y-%m-%d'])
    date_to = serializers.DateField(input_formats=['%Y-%m-%d'])
    source_currency = serializers.CharField(max_length=3)

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        if date_from >= date_to:
            raise serializers.ValidationError("date_from must be before date_to")

        return data

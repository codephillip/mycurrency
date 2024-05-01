from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CurrencyExchangeRate

from .serializers import CurrencyRateQueryParamsSerializer


class CurrencyRateListView(APIView):
    def get(self, request):
        query_params_serializer = CurrencyRateQueryParamsSerializer(data=request.query_params)
        if query_params_serializer.is_valid():
            validated_data = query_params_serializer.validated_data
            date_from = validated_data['date_from']
            date_to = validated_data['date_to']
            source_currency = validated_data['source_currency']

            currency_exchanges = CurrencyExchangeRate.objects.filter(
                valuation_date__range=(date_from, date_to),
                source_currency__code=source_currency
            ).select_related('exchanged_currency')

            response = {}
            for currency_exchange in currency_exchanges:
                currency_code = currency_exchange.exchanged_currency.code
                if currency_code not in response:
                    response[currency_code] = []
                response[currency_code].append({
                    'date': str(currency_exchange.valuation_date),
                    'value': float(currency_exchange.rate_value)
                })

            return Response({'data': {'source': source_currency, 'exchanges': response}})
        return Response(status=400, data=query_params_serializer.errors)

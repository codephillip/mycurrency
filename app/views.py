from collections import defaultdict
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CurrencyExchangeRate

from .serializers import CurrencyRateQueryParamsSerializer, CurrencyConverterSerializer
from .services.currency_service import currency_converter


class CurrencyRatePerCurrencyView(APIView):
    def get(self, request):
        serializer = CurrencyRateQueryParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            date_from = validated_data['date_from']
            date_to = validated_data['date_to']
            source_currency = validated_data['source_currency'].upper()

            currency_exchanges = CurrencyExchangeRate.objects.filter(
                valuation_date__range=(date_from, date_to),
                source_currency__code=source_currency
            ).select_related('exchanged_currency')

            response_data = defaultdict(list)
            for currency_exchange in currency_exchanges:
                currency_code = currency_exchange.exchanged_currency.code
                response_data[currency_code].append({
                    'date': str(currency_exchange.valuation_date),
                    'value': float(currency_exchange.rate_value)
                })

            return Response({'data': {'source': source_currency, 'exchanges': response_data}})
        return Response(status=400, data=serializer.errors)


class CurrencyConverterView(APIView):
    def get(self, request):
        serializer = CurrencyConverterSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            source_currency = data['source_currency'].upper()
            amount = data['amount']
            exchanged_currency = data['exchanged_currency'].upper()

            result = currency_converter(source_currency, amount, exchanged_currency)
            if result:
                exchanged_amount, exchange_rate = result
                response_data = {
                    'source_currency': source_currency,
                    'amount': amount,
                    'exchanged_currency': exchanged_currency,
                    'exchanged_amount': exchanged_amount,
                    'exchange_rate': exchange_rate
                }
                return Response({'data': response_data})
            return Response(status=400, data={'error': 'Failed to convert'})
        return Response(status=400, data=serializer.errors)

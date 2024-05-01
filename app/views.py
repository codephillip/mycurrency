from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CurrencyRateQueryParamsSerializer, CurrencyConverterSerializer
from .services.currency_service import get_currency_exchanges, currency_converter_response


class CurrencyRatePerCurrencyView(APIView):
    def get(self, request):
        serializer = CurrencyRateQueryParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            date_from = validated_data['date_from']
            date_to = validated_data['date_to']
            source_currency = validated_data['source_currency'].upper()
            response_data = get_currency_exchanges(date_from, date_to, source_currency)
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
            response_data = currency_converter_response(source_currency, amount, exchanged_currency)
            if response_data:
                return Response({'data': response_data})
            return Response(status=400, data={'error': 'Failed to convert'})
        return Response(status=400, data=serializer.errors)

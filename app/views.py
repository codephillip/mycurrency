from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CurrencyRateQueryParamsSerializer, CurrencyConverterSerializer
from .services.currency_service import get_currency_exchanges, format_currency_converter_response


class CurrencyRatePerCurrencyView(APIView):
    def get(self, request):
        serializer = CurrencyRateQueryParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = get_currency_exchanges(data['date_from'],
                                                   data['date_to'],
                                                   data['source_currency'].upper())
            return Response({'data': {'source': data['source_currency'].upper(), 'exchanges': response_data}})
        return Response(status=400, data=serializer.errors)


class CurrencyConverterView(APIView):
    def get(self, request):
        serializer = CurrencyConverterSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = format_currency_converter_response(data['source_currency'].upper(),
                                                               data['amount'],
                                                               data['exchanged_currency'].upper())
            if response_data:
                return Response({'data': response_data})
            return Response(status=400, data={'error': 'Failed to convert'})
        return Response(status=400, data=serializer.errors)

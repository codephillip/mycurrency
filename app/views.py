import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mycurrency.constants import UPLOAD_SUCCESS, NOT_FOUND, INVALID_JSON, CONVERSION_FAILED
from .serializers import CurrencyRateParamsSerializer, CurrencyConverterParamsSerializer, TWRRParamsSerializer, \
    CurrencyExchangeRateSerializer
from .services.currency_service import get_currency_exchanges, format_currency_converter_response, calculate_twrr
from datetime import datetime


class CurrencyRatePerCurrencyView(APIView):
    def get(self, request):
        serializer = CurrencyRateParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = get_currency_exchanges(data['date_from'],
                                                   data['date_to'],
                                                   data['source_currency'].upper())
            return Response({'data': {'source': data['source_currency'].upper(), 'exchanges': response_data}})
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class CurrencyConverterView(APIView):
    def get(self, request):
        serializer = CurrencyConverterParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = format_currency_converter_response(data['source_currency'].upper(),
                                                               data['amount'],
                                                               data['exchanged_currency'].upper())
            if response_data:
                return Response({'data': response_data})
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': CONVERSION_FAILED})
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class TWRRView(APIView):
    def get(self, request):
        serializer = TWRRParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            twrr_series = calculate_twrr(data['source_currency'],
                                         data['amount'],
                                         data['exchanged_currency'],
                                         data['start_date'],
                                         data.get('end_date', datetime.now()))
            return Response({'data': twrr_series})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadExchangesJson(APIView):
    def post(self, request):
        try:
            json_data = json.loads(request.data['json_file'].read().decode('utf-8'))
            serializer = CurrencyExchangeRateSerializer(data=json_data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': ('%s' % UPLOAD_SUCCESS)}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': NOT_FOUND}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({'error': INVALID_JSON}, status=status.HTTP_400_BAD_REQUEST)

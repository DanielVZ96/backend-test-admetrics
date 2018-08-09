import decimal

from abc import ABC
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer
from django.utils import timezone

from .models import ClpUsdRate

class Converter(APIView, ABC):
    """
    Abstract class for currency conversion. Subclasses have to define self.currency.
    Subclasses have to have a <currency>_conversion method available in the ClpUsdRate model.
    """

    #renderer_classes = (JSONRenderer, )

    @property
    def currency(self):
        try:
            return self.currency
        except AttributeError:
            raise NotImplementedError('Subclasses must set a currency string attribute.')

    def get(self, request):
        value = request.GET.get(self.currency, False)
        date = request.GET.get('date', False)
        if value and date:
            exact = True
            # Convert variables to date and decimal types
            try:
                date = timezone.datetime.strptime(date, '%Y%m%d')
            except ValueError:
                return Response("400: Date value doesn't make sense.", status=status.HTTP_400_BAD_REQUEST)
            value = decimal.Decimal(value)

            # Get rate by date.
            try:
                rate = ClpUsdRate.objects.get(date__day=date.day, date__month=date.month, date__year=date.year)
            except ClpUsdRate.DoesNotExist:
                return Response("404: we don't have any rate recorded for that date.", status=status.HTTP_404_NOT_FOUND)

            # If rate is None replace with closest past rate.
            if rate.clp_rate is None:
                rate = self.__get_past_rate(date)
                date = rate.date
                exact = False

            # Get conversion method from model and convert.
            converter = getattr(rate, '{}_conversion'.format(self.currency))
            new_value = converter(value)

            data = {
                'value': new_value,
                'exact_date': exact,
                'date': date,
            }

            return Response(data)
        else:
            return Response('No {} or date parameter found.'.format(self.currency), status=400)

    def __get_past_rate(self, date):
        rates = ClpUsdRate.objects.filter(date__lt=date).exclude(clp_rate=None)
        return rates.latest(field_name='date')


class UsdToClp(Converter):
    currency = 'usd'


class ClpToUsd(Converter):
    currency = 'clp'

import decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import ClpUsdRate


# Create your views here.
class UsdToClp(APIView):

    def get(self, request):
        """
         Returns usd value converted into a clp value for a given date. If nothing gets passed in url parameters, send error.
        """
        usd = request.GET.get('usd', False)
        date = request.GET.get('date', False)
        if usd and date:
            date = timezone.datetime.strptime(date, '%Y%m%d')
            usd = decimal.Decimal(usd)
            rate = ClpUsdRate.objects.get(date__day=date.day, date__month=date.month, date__year=date.year)
            return Response(rate.usd_to_clp(usd), status=200)
        else:
            return Response('No usd or date parameter found.',status=400)


class ClpToUsd(APIView):

    def get(self, request):
        """
         Returns clp value converted into a usd value for a given date. If nothing gets passed in url parameters, send error.
        """
        clp = request.GET.get('clp', False)
        date = request.GET.get('date', False)
        if clp and date:
            date = timezone.datetime.strptime(date, '%Y%m%d')
            clp = decimal.Decimal(clp)
            rate = ClpUsdRate.objects.get(date__day=date.day, date__month=date.month, date__year=date.year)
            return Response(rate.clp_to_usd(clp))
        else:
            return Response('No clp or date parameter found.',status=400)



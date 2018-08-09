import decimal

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.six import StringIO, BytesIO

from rest_framework.test import APITestCase
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, HTMLFormRenderer, BrowsableAPIRenderer

from .models import ClpUsdRate


class TestClpUsdRate(TestCase):


    def setUp(self):
        ClpUsdRate.objects.create(date=timezone.datetime(2000, 1, 1), clp_rate=538.22)
        ClpUsdRate.objects.create(date=timezone.datetime(2017, 12, 31), clp_rate=615.22)
        ClpUsdRate.objects.create(date= timezone.now() + timezone.timedelta(5), clp_rate=None)

    def test_values(self):
        jan_1_1996 = ClpUsdRate.objects.get(date=timezone.datetime(2000, 1, 1))
        dic_31_2017 = ClpUsdRate.objects.get(date=timezone.datetime(2017, 12, 31))
        future_date = ClpUsdRate.objects.get(date=timezone.now() + timezone.timedelta(5))

        self.assertEqual(jan_1_1996.clp_rate, decimal.Decimal("538.22"))
        self.assertEqual(dic_31_2017.usd_rate, decimal.Decimal("0.0016"))
        self.assertEqual(future_date.clp_rate, None)

    def test_convert_value(self):
        jan_1_1996 = ClpUsdRate.objects.get(date=timezone.datetime(2000, 1, 1))
        dic_31_2017 = ClpUsdRate.objects.get(date=timezone.datetime(2017, 12, 31))

        # Assert rates are reciprocal
        self.assertAlmostEqual(dic_31_2017.usd_rate * dic_31_2017.clp_rate, decimal.Decimal(1),
                               delta=decimal.Decimal(0.02))
        # Assert conversions work
        self.assertAlmostEqual(jan_1_1996.usd_conversion(2), decimal.Decimal(538.22*2), delta=decimal.Decimal(0.01))
        self.assertAlmostEqual(jan_1_1996.usd_conversion(0.5), decimal.Decimal(538.22/2), delta=decimal.Decimal(0.01))

        self.assertAlmostEqual(dic_31_2017.usd_conversion(2), decimal.Decimal(615.22*2), delta=decimal.Decimal(0.01))
        self.assertAlmostEqual(dic_31_2017.usd_conversion(0.5), decimal.Decimal(615.22/2), delta=decimal.Decimal(0.01))


class TestUpdateRates(TestCase):

    def test_command_output(self):
        out = StringIO()
        call_command('updaterates', stdout=out)
        self.assertIn('Successfully updated rates!', out.getvalue())

    def test_saves_all_dates(self):
        call_command('updaterates', all=True)
        for year in range(1990, timezone.now().year+1):
            rates = ClpUsdRate.objects.filter(date__year=year)
            self.assertAlmostEqual(len(rates), 358, delta=2, msg='Problem with {}'.format(year))


# API Tests

class TestConvertRates(APITestCase):
    def setUp(self):
        call_command('updaterates', all=True)

    def test_clp_response(self):
        url = reverse('clp')
        response = self.client.get(url + '?usd=2.5&date=20000127')
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        print(data)
        expected_value = 2.5*516.55
        self.assertAlmostEqual(float(data['value']), expected_value, delta=1)

    def test_usd_response(self):
        url = reverse('usd')
        response = self.client.get(url + '?clp=516.55&date=20000127')
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        print(data)
        expected_value = 1
        self.assertAlmostEqual(float(data['value']), expected_value, delta=1)

    def test_none_response(self):
        url = reverse('clp')
        response = self.client.get(url + '?usd=2&date=20120101')
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        print(data)
        self.assertEqual(data['value'], 1042.92)
        self.assertEqual(data['exact_date'], False)


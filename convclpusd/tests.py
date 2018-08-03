from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO
from django.db.models import DateField
from .models import ClpUsdRate
from datetime import date, timedelta


class TestClpUsdRate(TestCase):

    def setUp(self):
        ClpUsdRate.objects.create(date=date(2000, 1, 1), clp=538.22)
        ClpUsdRate.objects.create(date=date(2017, 12, 31), clp=615.22)
        ClpUsdRate.objects.create(date= timezone.now() + timedelta(5), clp=None)

    def test_values(self):
        jan_1_1996 = ClpUsdRate.objects.get(date=date(2000, 1, 1))
        dic_31_2017 = ClpUsdRate.objects.get(date=date(2017, 12, 31))
        future_date = ClpUsdRate.objects.get(date=timezone.now() + timedelta(5))

        self.assertEqual(jan_1_1996.usd_value, 538.22)
        self.assertEqual(dic_31_2017.clp_value, 0.0018)
        self.assertEqual(future_date.clp_value, None)

    def test_convert_value(self):
        jan_1_1996 = ClpUsdRate.objects.get(date=date(2000, 1, 1))
        dic_31_2017 = ClpUsdRate.objects.get(date=date(2017, 12, 31))

        self.assertAlmostEqual(jan_1_1996.usd_to_clp(2), 538.22*2, delta=0.01)
        self.assertAlmostEqual(jan_1_1996.usd_to_clp(0.5), 538.22/2, delta=0.01)

        self.assertAlmostEqual(dic_31_2017.usd_to_clp(2), 615.22*2, delta=0.01)
        self.assertAlmostEqual(dic_31_2017.usd_to_clp(0.5), 615.22/2, delta=0.01)


class TestUpdateRates(TestCase):

        def test_command_output(self):
            out = StringIO()
            call_command('updaterates', stdout=out)
            self.assertIn('Successfully updated rates', out.getvalue())

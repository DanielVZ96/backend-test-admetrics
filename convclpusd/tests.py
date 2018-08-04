from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO
from django.db.models import DateField
from .models import ClpUsdRate
from datetime import date, timedelta
import decimal


class TestClpUsdRate(TestCase):

    def setUp(self):
        ClpUsdRate.objects.create(date=date(2000, 1, 1), clp_rate=538.22)
        ClpUsdRate.objects.create(date=date(2017, 12, 31), clp_rate=615.22)
        ClpUsdRate.objects.create(date= timezone.now() + timedelta(5), clp_rate=None)

    def test_values(self):
        jan_1_1996 = ClpUsdRate.objects.get(date=date(2000, 1, 1))
        dic_31_2017 = ClpUsdRate.objects.get(date=date(2017, 12, 31))
        future_date = ClpUsdRate.objects.get(date=timezone.now() + timedelta(5))

        self.assertEqual(jan_1_1996.clp_rate, decimal.Decimal("538.22"))
        self.assertEqual(dic_31_2017.usd_rate, decimal.Decimal("0.0016"))
        self.assertEqual(future_date.clp_rate, None)

    def test_convert_value(self):
        jan_1_1996 = ClpUsdRate.objects.get(date=date(2000, 1, 1))
        dic_31_2017 = ClpUsdRate.objects.get(date=date(2017, 12, 31))

        # Assert rates are reciprocal
        self.assertAlmostEqual(dic_31_2017.usd_rate * dic_31_2017.clp_rate, decimal.Decimal(1),
                               delta=decimal.Decimal(0.02))
        # Assert conversions work
        self.assertAlmostEqual(jan_1_1996.usd_to_clp(2), decimal.Decimal(538.22*2), delta=decimal.Decimal(0.01))
        self.assertAlmostEqual(jan_1_1996.usd_to_clp(0.5), decimal.Decimal(538.22/2), delta=decimal.Decimal(0.01))

        self.assertAlmostEqual(dic_31_2017.usd_to_clp(2), decimal.Decimal(615.22*2), delta=decimal.Decimal(0.01))
        self.assertAlmostEqual(dic_31_2017.usd_to_clp(0.5), decimal.Decimal(615.22/2), delta=decimal.Decimal(0.01))



class TestUpdateRates(TestCase):

        def test_command_output(self):
            out = StringIO()
            call_command('updaterates', stdout=out)
            self.assertIn('Successfully updated rates', out.getvalue())

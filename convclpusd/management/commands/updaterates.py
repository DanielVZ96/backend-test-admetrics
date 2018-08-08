import datetime
import decimal
from django.core.management.base import BaseCommand
from convclpusd.models import ClpUsdRate as Rate
from ._sii_rates_scrapper import RateFetcher


class Command(BaseCommand):
    help = 'Updates the rates database with info from www.sii.cl, ' \
           'by bulk deleting the relevant objects and bulk creating them.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            '-a',
            action='store_true',
            help='Update all historical exchange rate data instead of current date data.'
        )

    def handle(self, *args, **options):
        if options['all']:
            all = True
            rates = RateFetcher(all_years=True).get_rate_list()
            with_all = 'all '
        else:
            all = False
            rates = RateFetcher(all_years=False).get_rate_list()
            with_all = ''

        rate_objects = []
        for rate in rates:
            date, clp_rate = rate
            if clp_rate is not None:
                clp_rate = decimal.Decimal(clp_rate)
                usd_rate = decimal.Decimal(1)/clp_rate
            else:
                usd_rate = None
            rate_objects.append(Rate(date=date, clp_rate=clp_rate, usd_rate=usd_rate))

        if all:
            Rate.objects.all().delete()
        else:
            Rate.objects.filter(date__year=datetime.datetime.now().year).delete()

        Rate.objects.bulk_create(rate_objects)

        self.stdout.write(self.style.SUCCESS('Successfully updated {}rates!').format(with_all))

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
        # Parse options and fetch rates accordingly.
        if options['all']:
            all = True
            rates = RateFetcher(all_years=True).get_rate_list()
            with_all = 'all '
        else:
            all = False
            rates = RateFetcher(all_years=False).get_rate_list()
            with_all = ''
        
        # Get all rate objects in a list in order to bulk_create them later
        rate_objects = []
        for rate in rates:
            date, clp_rate = rate
            if clp_rate is not None:
                clp_rate = decimal.Decimal(clp_rate)
                usd_rate = decimal.Decimal(1)/clp_rate
            else:
                usd_rate = None
            rate_objects.append(Rate(date=date, clp_rate=clp_rate, usd_rate=usd_rate))
        
        # Bulk delete objects that will be overridden (using bulk_create has this caveat, but it's still faster.)
        if all:
            Rate.objects.all().delete()
        else:
            Rate.objects.filter(date__year=datetime.datetime.now().year).delete()
        # Bulk_create rate objects.
        Rate.objects.bulk_create(rate_objects)

        self.stdout.write(self.style.SUCCESS('Successfully updated {}rates!').format(with_all))

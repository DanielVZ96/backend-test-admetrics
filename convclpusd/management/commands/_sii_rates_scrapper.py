import datetime
import decimal
import asyncio
import aiohttp
import lxml
from bs4 import BeautifulSoup
import re


class RateFetcher:
    """
    Class for fetching rates from sii.
    """
    CURRENT_URL = 'http://www.sii.cl/valores_y_fechas/dolar/dolar{}.htm'
    PREVIOUS_YEARS_URL = 'http://www.sii.cl/pagina/valores/dolar/dolar{}.htm'

    def __init__(self, all_years=False):
        self.rates = []
        current_year = datetime.datetime.now().year
        if all_years:
            self.years = [i for i in range(1990, current_year)]
        else:
            self.years = [current_year]

    async def year_rate_finder(self, year, response):
        """
        Finds rates in the response and appends them into self.rates in a (date,rate) tuple.
        """

        soup = BeautifulSoup(response, features='lxml')
        # Iteration by day:
        for d in range(1, 31):
            date_th_tag = soup.find(id='f{}'.format(d))
            reg = re.compile('^[0-9\.]+$')  # Regex that matches strings with only digits and dots('.').

            # Iteration by month and siblings of date th tag(<th id='f{d}' ... > {d} </th>):
            for m, sibling in zip(range(1, 13), date_th_tag.find_next_siblings()):
                rate = sibling.text.strip(" ").replace(',', '.')
                if not reg.match(rate):  # None for strings that don't match ^[0-9\.]+&
                    rate = None
                try:
                    date = datetime.date(year=int(year), month=m, day=d)
                    self.rates.append((date, rate))
                except ValueError:  # In order to handle non-existing dates.
                    continue

    async def fetch(self, session, year):
        """
        Fetches the response for a single year in www.sii.cl
        """

        if year < 2013:
            url = self.PREVIOUS_YEARS_URL.format(year)
        else:
            url = self.CURRENT_URL.format(year)

        async with session.get(url) as response:
            text = await response.text()
        await session.close()
        return str(text)

    async def rate_generator(self, year, session):
        """
        Fetches and finds rate in the year specified,
        """
        response = await self.fetch(session, year)
        await self.year_rate_finder(year, response)

    async def main(self):
        rate_generators = []
        for year in self.years:
            session = aiohttp.ClientSession()
            rate_generators.append(asyncio.ensure_future(self.rate_generator(year, session)))
        await asyncio.gather(*rate_generators)

    def get_rate_list(self):
        """
        Runs the main loop and when finished returns the rates
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
        return self.rates

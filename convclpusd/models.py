from django.db import models
import decimal


class ClpUsdRate(models.Model):
    date = models.DateField()
    clp_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # USD value in CLP E.g.: 538 clp
    usd_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True)  # CLP value in USD E.g.: 0.0016 usd

    def clp_to_usd(self, clp):
        """
        Receives clp value, converts it into usd and returns it.
        """
        return decimal.Decimal(decimal.Decimal(clp)*self.usd_rate)  # Eg: x usd = 1 usd * y clp / 538 clp

    def usd_to_clp(self, usd):
        """
        Receives usd value, converts it into clp and returns it.
        """
        return decimal.Decimal(decimal.Decimal(usd)*self.clp_rate)  # Eg: x clp = 1 clp * y usd / 0.0016 usd

    def save(self, *args, **kwargs):
        if self.clp_rate is not None:
            self.usd_rate = 1/self.clp_rate
        super(ClpUsdRate, self).save()


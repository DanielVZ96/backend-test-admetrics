from django.db import models
import decimal

DECIMAL_CONTEXT = decimal.getcontext()
DECIMAL_CONTEXT.prec =

class ClpUsdRate(models.Model):
    date = models.DateField()
    usd = models.DecimalField(max_digits=10, decimal_places=4)
    clp = models.DecimalField(max_digits=8, decimal_places=2)

    def usd_to_clp(self, usd):
        return decimal(self.clp * usd, )





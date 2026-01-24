from django.db import models
from decimal import Decimal, ROUND_DOWN


class Entity(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # store unit price as Decimal with 4 decimal places to preserve precision from measurements
    unit_price = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.name or self.pk}"

    @property
    def unit_price_decimal(self) -> Decimal:
        """Return the stored unit_price as Decimal."""
        # ensure we always return a Decimal instance
        val = self.unit_price
        try:
            return Decimal(val)
        except Exception:
            return Decimal(str(val or '0'))

    @property
    def unit_price_float(self) -> float:
        """Return the stored unit_price as float (convenience only)."""
        return float(self.unit_price_decimal)

    def price_cents_truncated(self) -> int:
        """Return price in cents after truncating to 2 decimal places (no rounding).

        Example: unit_price = Decimal('1.8640') -> truncates to 1.86 -> returns 186
        """
        val = self.unit_price_decimal.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return int((val * 100).to_integral_value())
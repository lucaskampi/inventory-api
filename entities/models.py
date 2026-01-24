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

    def unit_price_float(self) -> float:
        """Return unit price as float for convenience (not used for storage)."""
        return float(self.unit_price or Decimal('0'))

    def price_cents_truncated(self) -> int:
        """Return price in cents after truncating to 2 decimal places (no rounding)."""
        val = (Decimal(self.unit_price or Decimal('0'))).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return int((val * 100).to_integral_value())
from decimal import Decimal
from django.db import migrations, models


def forwards(apps, schema_editor):
    Entity = apps.get_model('entities', 'Entity')
    for obj in Entity.objects.all():
        # convert existing price_cents (int) to unit_price Decimal (defensive)
        try:
            cents = getattr(obj, 'price_cents', None)
            if cents is None:
                continue
            # handle strings/decimals/ints
            d = Decimal(str(cents))
            obj.unit_price = (d / Decimal('100')).quantize(Decimal('0.0001'))
            obj.save(update_fields=['unit_price'])
        except Exception:
            # skip problematic rows but continue migration
            continue


def backwards(apps, schema_editor):
    Entity = apps.get_model('entities', 'Entity')
    for obj in Entity.objects.all():
        try:
            val = getattr(obj, 'unit_price', None)
            if val is None:
                continue
            d = Decimal(str(val))
            obj.price_cents = int((d * Decimal('100')).to_integral_value())
            obj.save(update_fields=['price_cents'])
        except Exception:
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_entity_price_cents'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='unit_price',
            # use a serializable default (string) in migration to avoid import-time issues
            field=models.DecimalField(decimal_places=4, default='0.0000', max_digits=12),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name='entity',
            name='price_cents',
        ),
    ]

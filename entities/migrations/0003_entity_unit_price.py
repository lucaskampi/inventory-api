from decimal import Decimal
from django.db import migrations, models


def forwards(apps, schema_editor):
    Entity = apps.get_model('entities', 'Entity')
    for obj in Entity.objects.all():
        # convert existing price_cents (int) to unit_price Decimal
        cents = getattr(obj, 'price_cents', None)
        if cents is not None:
            obj.unit_price = Decimal(cents) / Decimal('100')
            obj.save(update_fields=['unit_price'])


def backwards(apps, schema_editor):
    Entity = apps.get_model('entities', 'Entity')
    for obj in Entity.objects.all():
        val = getattr(obj, 'unit_price', None)
        if val is not None:
            obj.price_cents = int((Decimal(val) * Decimal('100')).to_integral_value())
            obj.save(update_fields=['price_cents'])


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_entity_price_cents'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='unit_price',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=12),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name='entity',
            name='price_cents',
        ),
    ]

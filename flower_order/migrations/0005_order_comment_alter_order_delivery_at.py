# Generated by Django 4.1.5 on 2023-01-20 17:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower_order', '0004_alter_order_bouquets_alter_order_delivery_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 17, 19, 0, 640820, tzinfo=datetime.timezone.utc), verbose_name='Когда доставить'),
        ),
    ]
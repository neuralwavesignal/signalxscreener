# Generated by Django 5.1.7 on 2025-03-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screeners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='cmp_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

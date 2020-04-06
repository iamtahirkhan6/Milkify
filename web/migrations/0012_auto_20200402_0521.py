# Generated by Django 3.0.4 on 2020-04-02 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20200401_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='duration_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='address_1',
            field=models.CharField(blank=True, max_length=500, verbose_name='address 1'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='address_2',
            field=models.CharField(blank=True, max_length=500, verbose_name='address 2'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='duration_till',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='timing',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '7AM'), (2, '8AM'), (3, '9AM'), (4, '10AM'), (5, '4PM'), (6, '5PM'), (7, '6PM'), (8, '7PM')], null=True, verbose_name='timing'),
        ),
    ]

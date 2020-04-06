# Generated by Django 3.0.4 on 2020-04-01 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20200328_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='address_1',
            field=models.CharField(blank=True, max_length=200, verbose_name='address 1'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='address_2',
            field=models.CharField(blank=True, max_length=200, verbose_name='address 2'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='locality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Locality'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='mobile',
            field=models.CharField(blank=True, max_length=250, verbose_name='mobile number'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='timing',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '6am'), (2, '7am'), (3, '8am'), (4, '9am'), (4, '4pm'), (5, '5pm'), (6, '6pm'), (7, '7pm')], null=True, verbose_name='timing'),
        ),
    ]
# Generated by Django 3.0.4 on 2020-03-26 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20200320_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]

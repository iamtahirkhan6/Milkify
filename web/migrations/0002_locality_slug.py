# Generated by Django 3.0.4 on 2020-03-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]

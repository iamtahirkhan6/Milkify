# Generated by Django 3.0.4 on 2020-03-27 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_remove_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('duration_till', models.DateField()),
                ('total_amount', models.FloatField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.0 on 2018-12-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_auto_20181223_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 2.0 on 2018-12-23 11:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_user_cart_exist'),
        ('Order', '0003_auto_20181221_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='para',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.ParaProfile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateField(default=datetime.date(2018, 12, 23)),
        ),
    ]
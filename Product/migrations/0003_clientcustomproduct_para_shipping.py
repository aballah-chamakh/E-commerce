# Generated by Django 2.0 on 2018-12-15 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_customerprofile_phone'),
        ('Product', '0002_auto_20181214_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcustomproduct',
            name='para_shipping',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.ParaProfile'),
        ),
    ]

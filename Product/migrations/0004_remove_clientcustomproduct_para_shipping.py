# Generated by Django 2.0 on 2018-12-27 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_clientcustomproduct_para_shipping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientcustomproduct',
            name='para_shipping',
        ),
    ]

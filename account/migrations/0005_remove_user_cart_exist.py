# Generated by Django 2.0 on 2018-12-15 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_customerprofile_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cart_exist',
        ),
    ]
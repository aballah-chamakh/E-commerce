# Generated by Django 2.0 on 2018-12-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_selling_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cart_exist',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.0 on 2018-12-14 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcustomproduct',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='paracustomproduct',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
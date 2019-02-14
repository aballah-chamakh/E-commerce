# Generated by Django 2.0 on 2018-12-13 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Cart.Cart')),
            ],
        ),
    ]

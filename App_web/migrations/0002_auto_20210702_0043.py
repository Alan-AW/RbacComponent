# Generated by Django 3.1.4 on 2021-07-01 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '客户表'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': '付费记录'},
        ),
        migrations.AlterModelTable(
            name='customer',
            table='customer',
        ),
        migrations.AlterModelTable(
            name='payment',
            table='payment',
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0004_auto_20211011_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='current_quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Current quantity'),
        ),
    ]

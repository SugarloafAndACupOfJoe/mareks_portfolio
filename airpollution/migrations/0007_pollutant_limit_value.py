# Generated by Django 3.1.4 on 2021-02-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airpollution', '0006_auto_20210127_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollutant',
            name='limit_value',
            field=models.SmallIntegerField(null=True),
        ),
    ]
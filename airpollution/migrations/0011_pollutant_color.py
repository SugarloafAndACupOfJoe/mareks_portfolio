# Generated by Django 3.1.4 on 2021-02-18 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airpollution', '0010_country_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollutant',
            name='color',
            field=models.CharField(default='#000000', max_length=10),
        ),
    ]

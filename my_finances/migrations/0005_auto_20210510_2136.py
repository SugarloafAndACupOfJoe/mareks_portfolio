# Generated by Django 3.1.4 on 2021-05-10 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_finances', '0004_auto_20210412_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='repetition_interval',
            field=models.PositiveSmallIntegerField(choices=[(1, 'N/A'), (2, 'DAYS'), (3, 'WEEKS'), (4, 'MONTHS'), (5, 'YEARS')], default=1, null=True),
        ),
    ]
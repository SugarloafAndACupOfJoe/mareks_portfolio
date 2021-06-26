# Generated by Django 3.1.4 on 2021-04-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_finances', '0003_auto_20210411_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='income',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

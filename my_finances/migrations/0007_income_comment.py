# Generated by Django 3.1.4 on 2021-05-10 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_finances', '0006_auto_20210510_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
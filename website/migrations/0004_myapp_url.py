# Generated by Django 3.1.4 on 2020-12-18 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20201206_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='myapp',
            name='url',
            field=models.CharField(default='/airpollution', max_length=30),
            preserve_default=False,
        ),
    ]

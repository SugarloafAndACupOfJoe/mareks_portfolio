# Generated by Django 3.1.4 on 2020-12-06 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_myapp_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myapp',
            name='image',
            field=models.ImageField(upload_to='my_apps'),
        ),
    ]

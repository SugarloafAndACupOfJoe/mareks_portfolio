# Generated by Django 3.1.4 on 2021-05-31 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_finances', '0011_auto_20210511_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outcome',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outcome',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='outcomes', to='auth.user'),
            preserve_default=False,
        ),
    ]

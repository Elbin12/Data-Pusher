# Generated by Django 5.1.7 on 2025-03-19 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_account_app_secret_token_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='app.account'),
        ),
        migrations.AddConstraint(
            model_name='destination',
            constraint=models.UniqueConstraint(fields=('account', 'url', 'http_method'), name='unique_account_url_method'),
        ),
    ]

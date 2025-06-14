# Generated by Django 5.1.7 on 2025-03-31 09:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_reason_fraudreport_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='fraudreport',
            old_name='description',
            new_name='reason',
        ),
        migrations.AlterField(
            model_name='fraudreport',
            name='reported_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_fraud', to=settings.AUTH_USER_MODEL),
        ),
    ]

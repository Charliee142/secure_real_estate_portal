# Generated by Django 5.1.7 on 2025-03-28 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_rentalprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rentalprice',
            options={'ordering': ['months']},
        ),
        migrations.RemoveField(
            model_name='property',
            name='price',
        ),
    ]

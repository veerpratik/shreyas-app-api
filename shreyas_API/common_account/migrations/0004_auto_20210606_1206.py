# Generated by Django 3.2 on 2021-06-06 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_account', '0003_auto_20210606_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]